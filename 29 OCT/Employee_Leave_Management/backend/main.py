from database import get_db_connection
from fastapi import FastAPI, HTTPException,status
from security import (
    verify_password,
    create_access_token,
    verify_access_token
)
from pydantic import BaseModel
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeaveDecision(BaseModel):
    decision: str
    comments: str = ""

class LeaveRequest(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str
class LoginRequest(BaseModel):
    username: str
    password: str

# JWT Bearer authentication
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):

    # Extract JWT from the Authorization header
    token = credentials.credentials

    # Verify the JWT
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # Get user ID from the token
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token information"
        )

    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Find the user in PostgreSQL
        cursor.execute(
            """
            SELECT user_id, employee_id, username,
                   email, role, is_active
            FROM users
            WHERE user_id = %s;
            """,
            (user_id,)
        )

        current_user = cursor.fetchone()

        # Check whether the account exists and is active
        if not current_user or not current_user["is_active"]:
            raise HTTPException(
                status_code=401,
                detail="User account is inactive or unavailable"
            )

        return current_user

    finally:
        connection.close()
leave_requests = []

@app.get("/")
def home():
    return {"message": "Employee Leave Management API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/leave-requests")
def create_leave_request(
    request: LeaveRequest,
    current_user=Depends(get_current_user)
):

    # Step 1: Validate the dates
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    # Step 2: Calculate calendar days
    total_days = (request.end_date - request.start_date).days + 1

    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Step 3: Insert request using authenticated employee ID
        cursor.execute(
            """
            INSERT INTO leave_requests (
                employee_id,
                leave_type_id,
                start_date,
                end_date,
                total_days,
                reason,
                status
            )
            SELECT
                %s,
                lt.leave_type_id,
                %s,
                %s,
                %s,
                %s,
                'PENDING'
            FROM leave_types lt
            WHERE lt.leave_name = %s
              AND lt.is_active = TRUE

            RETURNING
                request_id,
                employee_id,
                leave_type_id,
                start_date,
                end_date,
                total_days,
                reason,
                status;
            """,
            (
                current_user["employee_id"],
                request.start_date,
                request.end_date,
                total_days,
                request.reason,
                request.leave_type
            )
        )

        # Step 4: Retrieve inserted request
        new_request = cursor.fetchone()

        if new_request is None:
            raise HTTPException(
                status_code=404,
                detail="Active leave type not found"
            )

        # Step 5: Save transaction
        connection.commit()

        return {
            "message": "Leave request submitted successfully",
            "leave_request": new_request
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

@app.get("/leave-requests")
def get_leave_requests(
    current_user=Depends(get_current_user)
):

    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Employee can view only their own requests
        if current_user["role"] == "EMPLOYEE":

            cursor.execute("""
                SELECT
                    lr.request_id AS id,
                    e.first_name,
                    e.last_name,
                    lt.leave_name AS leave_type,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status
                FROM leave_requests lr

                JOIN employees e
                    ON lr.employee_id = e.employee_id

                JOIN leave_types lt
                    ON lr.leave_type_id = lt.leave_type_id

                WHERE lr.employee_id = %s

                ORDER BY lr.applied_at DESC;
            """, (current_user["employee_id"],))

        else:
            # Temporary: Managers and HR can view all requests.
            # We will implement their separate access rules later.

            cursor.execute("""
                SELECT
                    lr.request_id AS id,
                    e.first_name,
                    e.last_name,
                    lt.leave_name AS leave_type,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status
                FROM leave_requests lr

                JOIN employees e
                    ON lr.employee_id = e.employee_id

                JOIN leave_types lt
                    ON lr.leave_type_id = lt.leave_type_id

                ORDER BY lr.applied_at DESC;
            """)

        leave_requests = cursor.fetchall()

        return leave_requests

    finally:
        connection.close()



@app.get("/leave-types")
def get_leave_types():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            leave_type_id,
            leave_name,
            description,
            default_days,
            is_paid
        FROM leave_types
        WHERE is_active = TRUE
        ORDER BY leave_type_id;
    """)

    leave_types = cursor.fetchall()

    cursor.close()
    connection.close()

    return leave_types



@app.get("/leave-balances")
def get_leave_balances(
    current_user=Depends(get_current_user)
):

    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                lt.leave_name AS leave_type,
                lb.total_allocated,
                lb.used_days,
                lb.remaining_days,
                lb.year
            FROM leave_balances lb

            JOIN employees e
                ON lb.employee_id = e.employee_id

            JOIN leave_types lt
                ON lb.leave_type_id = lt.leave_type_id

            WHERE e.employee_id = %s
              AND lb.year = 2026

            ORDER BY lb.balance_id;
        """, (current_user["employee_id"],))

        balances = cursor.fetchall()

        return balances

    finally:
        connection.close()


@app.post("/leave-requests/{request_id}/decision")
def decide_leave_request(
    request_id: int,
    decision_data: LeaveDecision,
    current_user=Depends(get_current_user)
):

    # Step 1: Check the user's role
    if current_user["role"] not in ["MANAGER", "HR_ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Only Managers and HR Admins can decide leave requests"
        )

    decision = decision_data.decision.upper()

    if decision not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Decision must be APPROVED or REJECTED"
        )

    # Step 2: Prevent managers from deciding their own requests
    if current_user["role"] == "MANAGER":
        connection = get_db_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT employee_id
                FROM leave_requests
                WHERE request_id = %s
                """,
                (request_id,)
            )

            request_owner = cursor.fetchone()

            if request_owner is None:
                raise HTTPException(
                    status_code=404,
                    detail="Leave request not found"
                )

            if request_owner["employee_id"] == current_user["employee_id"]:
                raise HTTPException(
                    status_code=403,
                    detail="Managers cannot decide their own leave requests"
                )

        finally:
            connection.close()

    # Step 3: Connect to PostgreSQL
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Find the pending leave request
        cursor.execute(
            """
            SELECT employee_id, leave_type_id, total_days,
                   EXTRACT(YEAR FROM start_date)::INT AS leave_year
            FROM leave_requests
            WHERE request_id = %s
              AND status = 'PENDING'
            FOR UPDATE;
            """,
            (request_id,)
        )

        leave_request = cursor.fetchone()

        if leave_request is None:
            raise HTTPException(
                status_code=404,
                detail="Pending leave request not found"
            )

        # Step 4: Record the decision using authenticated manager ID
        cursor.execute(
            """
            INSERT INTO leave_approvals (
                request_id,
                approver_user_id,
                decision,
                comments
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                request_id,
                current_user["user_id"],
                decision,
                decision_data.comments
            )
        )

        # Step 5: Update the leave request status
        cursor.execute(
            """
            UPDATE leave_requests
            SET status = %s
            WHERE request_id = %s;
            """,
            (decision, request_id)
        )

        # Step 6: Update leave balance only when approved
        if decision == "APPROVED":

            cursor.execute(
                """
                UPDATE leave_balances
                SET used_days = used_days + %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE employee_id = %s
                  AND leave_type_id = %s
                  AND year = %s;
                """,
                (
                    leave_request["total_days"],
                    leave_request["employee_id"],
                    leave_request["leave_type_id"],
                    leave_request["leave_year"]
                )
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Leave balance record not found"
                )

        # Step 7: Commit all changes
        connection.commit()

        return {
            "message": f"Leave request {decision.lower()} successfully",
            "request_id": request_id,
            "decision": decision
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


@app.post("/login")
def login(user: LoginRequest):

    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        # Find the user in PostgreSQL
        cursor.execute(
            """
            SELECT user_id, employee_id, username,
                   email, password_hash, role, is_active
            FROM users
            WHERE username = %s;
            """,
            (user.username,)
        )

        db_user = cursor.fetchone()

        # Check whether the user exists and is active
        if not db_user or not db_user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # Verify the entered password
        password_correct = verify_password(
            user.password,
            db_user["password_hash"]
        )

        if not password_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        # Prepare user information for the JWT
        token_data = {
            "sub": str(db_user["user_id"]),
            "user_id": db_user["user_id"],
            "employee_id": db_user["employee_id"],
            "username": db_user["username"],
            "role": db_user["role"]
        }

        # Generate JWT
        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": db_user["user_id"],
                "employee_id": db_user["employee_id"],
                "username": db_user["username"],
                "email": db_user["email"],
                "role": db_user["role"]
            }
        }

    finally:
        connection.close()
@app.get("/profile")
def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Authentication successful!",
        "user": {
            "user_id": current_user["user_id"],
            "username": current_user["username"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    }
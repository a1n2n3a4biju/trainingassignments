
import redis
import json

# Connect to Redis running in Docker
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# Check Redis connection
def check_redis():
    return r.ping()


# Save a chat message
def save_message(session_id, role, message):
    key = f"chat:{session_id}"

    chat_message = {
        "role": role,
        "message": message
    }

    r.rpush(key, json.dumps(chat_message))

    # Keep only the latest 10 messages
    r.ltrim(key, -10, -1)


# Retrieve chat history
def get_chat_history(session_id):
    key = f"chat:{session_id}"

    messages = r.lrange(key, 0, -1)

    return [
        json.loads(message)
        for message in messages
    ]


# Test the connection and memory
if __name__ == "__main__":

    print("Redis connected:", check_redis())

    save_message(
        "session_001",
        "user",
        "What is the weather in Jaipur?"
    )

    save_message(
        "session_001",
        "assistant",
        "Jaipur is expected to be warm."
    )

    history = get_chat_history("session_001")

    print("\nChat History:")

    for message in history:
        print(message)

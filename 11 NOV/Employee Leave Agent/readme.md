Employee- Leave -Policy

1.Azure:
MS Foundry->create->Foundry portal->instructions->upload file->guardrails->sample questions->traces->create resourse

2.Come to pycharm:
copy FOUNDRY_PROJECT_ENDPOINT to .env
install requirements
update main.py
in terminal:
    az config set core.enable_broker_on_windows=false    
    az login      
run main.py
type sample questions in terminal
go to traces in portal and check the tracing

3.Open Docker for redis
update requirements.txt
update main.py
add redis url to .env
in terminal:
    docker run -d --name retail-redis -p 127.0.0.1:6379:6379 -v retail_redis_data:/data redis:7-alpine redis-server --appendonly yes 
in new terminal:
    python -m uvicorn main:app --reload 
go to http://127.0.0.1:8000/docs?utm_source=chatgpt.com#/default/get_history_history__session_id__get:
    post message
    copy session id and paste with next message
    copy session id and paste on get/history
    verify history
come back to pycharm open new terminal:
     docker exec -it retail-redis redis-cli
    127.0.0.1:6379> KEYS retail:*
it should show the histories

-----------------------------------------------------------------------
    

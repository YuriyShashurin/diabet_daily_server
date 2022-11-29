from multiprocessing import cpu_count


# Socket Path

bind = 'unix:/root/projects/diabet_daily_server/gunicorn.sock'



# Worker Options

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'



# Logging Options

loglevel = 'debug'

accesslog = '/root/projects/diabet_daily_server/access_log'

errorlog =  '/root/projects/diabet_daily_server/error_log'

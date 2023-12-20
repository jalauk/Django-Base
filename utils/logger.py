from django.utils.timezone import localtime
from django.conf import settings
from loguru import logger
from .constants import Constant
from pytz import timezone


class Logger:
    base_path = f'{settings.BASE_DIR}/logs/{{time:D-MMM-YYYY}}'

    # logFile = f"{settings.BASE_DIR}/logs/{{time:D-MMM-YYYY}}.log"
    logger.add(f'{base_path}/request.log', format="{message}", rotation="1 days", level="INFO")
    logger.add(f'{base_path}/error.log', format="{message}", rotation="1 days", level="INFO")

    request_log = logger.bind(name="request")
    error_log = logger.bind(name="error")

    @classmethod
    def log(cls, request, response, timeTaken=None):
        # if settings.DEBUG:
        #     return None
        currentTime = localtime(timezone=timezone(
            "Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        data = f"""
            {currentTime} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {request.headers}\n"""
        print("this")
        if timeTaken is not None:
            print("our")
            data += f"""STATUS [{response.data.get('status')}] | STATUS_CODE [{response.data.get('code')} ~ {Constant.responseMessages[response.data.get('code')]}] | TIME_TAKEN [{round(timeTaken, 3)} Seconds]\n"""     # noqa
            data += "\n************************************************************************************************************"   # noqa
            cls.request_log.info(data.replace('  ', ''))
        else:
            print("working")
            data += f"""STATUS [False] | STATUS_CODE [500 ~ Server Error]

            xxxxxxxxxxxxxxxxxxxx [ERROR] xxxxxxxxxxxxxxxxxxxxxxxxxx
            {response}"""
            # SES.sendDev(
            #     time=currentTime,
            #     userAgent=request.headers.get('User-Agent'),
            #     ip=request.META.get('REMOTE_ADDR'),
            #     apiEndpoint=request.build_absolute_uri(),
            #     apiMethod=request.method,
            #     error=response
            # )
            data += "\n************************************************************************************************************"   # noqa
            cls.error_log.info(data.replace('  ', ''))

from fastapi.responses import JSONResponse

class ResponseInfo:
    '''
    This is the custom response class. It contains two methods:
    -success_res: This method is called when we need to return a successful response.
    -error_res: This method is called when we need to return error messages.
    '''
    def __init__(self, data=[], success=True, message=None, status_code=None):
        self.data = data
        self.message = message
        self.success = success
        self.status_code = status_code

    def success_res(self):
        return JSONResponse({
                "data": self.data,
                "success": self.success,
                "message": self.message,
                "status_code": self.status_code}
            )

    def errro_res(self):
        return JSONResponse({
                "data": self.data,
                "success": self.success,
                "message": self.message,
                "status_code": self.status_code}
            )

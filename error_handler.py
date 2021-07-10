from utils import handle_page

def unauthorized(e):
    return handle_page('http-error.html',
                           error="401 - Unauthorized", error_description="You're unauthorized to perform this action.\n"
                                                                         "Please contact the us at "
                                                                         "support@learnearnfun.com if you feel this is "
                                                                         "an issue"), 401

def forbidden(e):
    return handle_page('http-error.html',
                           error="403 - Forbidden", error_description="You're unauthorized to perform this action.\n"
                                                                      "Please contact the us at "
                                                                      "support@learnearnfun.com if you feel this is an "
                                                                      "issue"), 403


def not_found(e):
    return handle_page('http-error.html',
                           error="404 - Page Not Found",
                           error_description="Sorry, The Resource you are looking for is not found",), 404


def internal_error(e):
    return handle_page('http-error.html',
                           error="500 - Internal Server Error",
                           error_description="An error has occurred on the System, Please Try Again\n"
                                             "We apologize for the inconvenience. "), 500


def bad_request(e):
    return handle_page('http-error.html',
                           error="400 - Bad Request", error_description="The browser sent a request that the server"
                                                                        " could not understand,"
                                                                        " we apologize for the inconvenience."), 400

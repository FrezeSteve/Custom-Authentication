def custom_set_cookie(request, response):
    if not request.get_signed_cookie('custom_session_id', default=None):
        if not (request.session and request.session.get('session_key')):
            request.session.save()
        value = request.session.session_key
        max_age = 60 * 60 * 60 * 24 * 30
        response.set_signed_cookie(
            "custom_session_id", value=value, max_age=max_age, expires=None, path='/'
            , domain=None, secure=None, httponly=True, samesite='Strict'
        )


def custom_set_cookie_for_user(response, session_id):
    max_age = 60 * 60 * 60 * 24 * 30
    response.set_signed_cookie(
        "custom_session_id", value=session_id, max_age=max_age, expires=None, path='/'
        , domain=None, secure=None, httponly=True, samesite='Strict'
    )

import sendgrid
from settings import SENDGRID_API_KEY, SENDGRID_EMAIL
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from sendgrid.helpers.mail import Mail

sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)


def send_dynamic_email(to_email, template_id, **kwargs):
    message = Mail(
        from_email=SENDGRID_EMAIL,
        to_emails=to_email
    )

    message.dynamic_template_data = kwargs
    message.template_id = template_id

    try:
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        raise HTTP_503_SERVICE_UNAVAILABLE
    return response.status_code

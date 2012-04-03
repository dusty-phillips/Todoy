
def setup():
    validate("#registration_form",
        {
        'confirm_password': 'The passwords do not match',
        'username': "I'm afraid that username is taken"},
        username={
            'required': True,
            'remote': 'user_valid.json'
        },
        password='required',
        confirm_password={'equalTo': 'input[name=password]'})


@JSVar('jQuery')
def validate(selector, mess=None, **kwargs):
    if mess == None:
        mess = {}
    jQuery(js(selector)).validate(
        {'rules': js(kwargs),
        'messages': js(mess)
        }
        )

jQuery(js(setup))

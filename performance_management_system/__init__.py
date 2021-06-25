class IntegerResource:
    HR_INDEX = 1000
    CLIENT_INDEX = 5000
    EMPLOYEE_INDEX = 6000

class StringResource:
    COMPANY_PREFIX_TAG = 'Globe'
    COMPANTY_EMAIL_SUFFIX = '@globe.com'
    
    CLIENT = 'Client'
    EMPLOYEE = 'Employee'
    HR_ADMIN = 'HR Admin'

LIST_MENU = [
    ['', 'All'],
    ['?filter=evaluated','Evaluated'],
    ['?filter=on evaluation','On Evaluation'],
]
DETAILS_MENU = [
    ['', 'Details'],
    ['clients', 'Clients'],
    ['pick-a-client','Pick a client'],
    ['evaluated','Evaluated'],
    ['on-evaluation','On Evaluation'],
]


IS_EVALUATED = [
    ('none', 'None'),
    ('evaluated', 'Evaluated'),
    ('on evaluation','On Evaluation')
]
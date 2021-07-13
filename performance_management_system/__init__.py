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

GRADIENT_BG = [
    ['#93EDC7', '#1CD8D2'],
    ['#F08787', '#FF3F3F'],
    ['#AD86FF', '#7C3FFF'],
    ['#7DDB97', '#00A62E'],
    ['#FFB9A3', '#EE3900'],
    ['#B3B1F4', '#0500EF'],
]
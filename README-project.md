# Warehouse

## Description

An example task, part of the assesment process of ICT Strypes.


## Requirements

- Python >= 3.12
- Poetry >= 1.8.3

If you wish **NOT** to use poetry as a dependancy manager, a full export of requirements.txt is provided in `dist/`

## Custom comment syntax:

In code serval keywords are being used:
- `ASSUME` - when the description wasn't clear, therefore I assumed the case and possibly explained additional variants.
- `TODO` - when I have the right way of doing this explained in the comment.
- `IDEA` - Explaining my tought process.

## Django settings

Location of the Django settings is the `settings/` directory. Since the settings will reamin the same in dev and prod, I decided to leave them as a single env configuration. However, for readability purposes, I've divided the sections into separate files. 

When going to production some settings, like the DB backend creds, logging engine, security hashes, ect need to be changed, the most secure way would be to have them pulled on deploy from a secure store and/or being deployed as ENV variables to the working environment. Credentials and salt hashes should never reamain in the code base itself.

### Authentication

The task metions the authentication to be by my own choice, since I din't want to configure Token based auth (eg. JWT). I've opt for
Basic and Session auth. Since Django 5.x deemed [GET /logout] as unsafe, I needed to patch/override the logout view.

The task said to use IsAuthenticated for the API, but I went out for IsAuthenticatedOrReadOnly, leveraging the Swagger login/logout capabilities.
No endpoint would return anything, without auth, only the method definition remains visible.

### API docs

Using the drf-yasg module, I've enabled swagger and redoc. Swagger supports both Session and Basic auth.

## Dictionary

### Common
- **Места** / **Зона** - `Storage Spaces` / `Storage space`
- **Отговорници (в склад)** - `Accountables (for a storage space)`
- **Длъжност (на отговорника)** - `Accountable Type`
- **Служител (на фирмата)** - `Employee`
- **Инвентарни Обекти** / **Неща** - `Items`


### Roles
- **служител** - `Staff` (can be modified, database record)
- **служител инвентар** - `Staff - inventory` (can be modified, database record)
- **администратор** - `Administrators` (can be modified, database record)

### Storage space priorities:
- **нисък** - `Low`
- **стандартен** - `Standard`
- **повишен** - `Raised`
- **висок** - `High`

### 

## Fixtures

- **Superuser**: `./manage.py loaddata warehouse/apps/core/fixtures/users.yaml`
- **Groups and Permissions**: `./manage.py warehouse/apps/core/fixtures/groups.yaml`

## TO-DOs

- Add docstrings to all custom defined methods and classes
- Add unit tests for models
- Add integration tests for API endpoints
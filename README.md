### Hexlet tests and linter status:
[![Actions Status](https://github.com/vadim-gusak/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/vadim-gusak/python-project-50/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/535aad6baa40bd73d379/maintainability)](https://codeclimate.com/github/vadim-gusak/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/535aad6baa40bd73d379/test_coverage)](https://codeclimate.com/github/vadim-gusak/python-project-50/test_coverage)
[![first_steps](https://github.com/vadim-gusak/python-project-50/actions/workflows/main.yml/badge.svg)](https://github.com/vadim-gusak/python-project-50/actions/workflows/main.yml)
# Вычислитель отличий
Добро пожаловать в мой [второй учебный проект](https://ru.hexlet.io/programs/python/projects/50) с портала Hexlet.io
## Описание

Вычислитель отличий – программа, определяющая разницу между двумя структурами данных.

Возможности утилиты:

- Поддержка разных входных форматов: yaml, json
- Генерация отчета в виде plain, stylish и json

Пример использования:
```
gendiff --format plain filepath1.json filepath2.yml

Setting "common.setting4" was added with value: False
Setting "group1.baz" was updated. From 'bas' to 'bars'
Section "group2" was removed
```

### Установка
Проект собран при помощи пакетного менеджера poetry ver. 1.2.1. В корневой директории находится Makefile с командами необходиммыми для установки.
Для начала выполнить сборку:
```commandline
make build
```
Далее установка:
```commandline
make package-install
```
### Использование
Программа ожидает на вход два файла с расширением .json или .yml/.yaml
По умолчанию утановлен форматер **stylish**. Команда для примера:
```commandline
gendiff file1.json file2.json
```
```commandline
gendiff -f stylish file1.json file2.json
```
Вывод будет таким:
```
{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}
```
Пример в виде аскинемы:

<a href="https://asciinema.org/a/527492" target="_blank"><img src="https://asciinema.org/a/527492.svg" /></a>

Форматер **plain**:
```commandline
gendiff -f plain file1.json file2.json
```
Его вывод:
```
Property 'follow' was removed
Property 'proxy' was removed
Property 'timeout' was updated. From 50 to 20
Property 'verbose' was added with value: true

```
Пример в виде аскинемы:

<a href="https://asciinema.org/a/527493" target="_blank"><img src="https://asciinema.org/a/527493.svg" /></a>

Также доступен вывод в виде **json** файла:
```commandline
gendiff -f json file1.json file2.json
```
```
{
  "follow_removed": false,
  "host": "hexlet.io",
  "proxy_removed": "123.234.53.22",
  "timeout": 50,
  "timeout_updated": 20,
  "verbose_added": true
}
```
Пример в виде аскинемы:

<a href="https://asciinema.org/a/527494" target="_blank"><img src="https://asciinema.org/a/527494.svg" /></a>

Вы можете использовать данную программу, как пакет к своему проекту. Функция **generate_diff** подготовлена для импорта.
Она ожидакт на вход три параметра:
- Первые два - это данные для сравнения
- Третий - тип форматера в виде строки: stylish, plain или json. По умолчанию установлен stylish.

В программе я использую встроенный парсер json файлов и PyYAML. 
Поэтому рефлизация функции основана на их представлении данных после парсинга.

Функция возвращает строку, как в примерах выше, в виде зависещем от форматера.

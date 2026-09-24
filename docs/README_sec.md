# security-actions

## Система релизов с тегами

Проект использует систему релизов с тегами. Версии релизов создаются автоматически с помощью semantic-release на основе изменений в коде. Для работы с релизами используется файл `release-tagging.yml`, который управляет созданием тегов версий (v1.2.3, latest, v1, v1.2).

## Как встроить в свой Pipeline

Нужно добавить include и указать с помощью stages, на каком этапе следует запускать сканеры.<br>
security_static можно запускать на любом этапе пайпланаим нужны только файлы в репозитории для проведения сканирования.<br>
security_dynamic требуют готовый артефакт или тестовую среду для запуска, их лучше вызывать перед или после тестов.

```
include:
  - project: devsecops/public-projects/security-actions
    ref: <VERSION_TAG>
    file: security-actions.yml

stages:
  - security_static
  - security_dynamic
```

## Как управлять Action'ами

Управлять можно через переопределение глобальных переменных.

Выключить экшн в пайплайне
```
  X5_SECURITY_PIPE_SEMGREP_DISABLE: "false"     # Чтобы отключить semgrep job, указать true
  X5_SECURITY_PIPE_GITLEAKS_DISABLE: "false"    # Чтобы отключить gitleaks job, указать true
  X5_SECURITY_PIPE_SYFT_DISABLE: "false"        # Чтобы отключить syft job, указать true
  X5_SECURITY_PIPE_TRIVY_FS_DISABLE: "true"     # По стандарту отключен, так как дублирует функционал syft и gitleaks с включенным secrets сканнером. указать false, что бы включить.
  X5_SECURITY_PIPE_TRIVY_IMAGE_DISABLE: "true"  # По стандарту отключен, так как не все пайплайны собирают образы контейнеров, если в вашем пайплайне собирается образ то рекомендуется включить.
  X5_SECURITY_PIPE_KCS_DISABLE: "true"          # По стандарту отключен. KCS сканирует контейнерный образ через scan-service; включите и укажите путь к образу.
  X5_SECURITY_PIPE_MOBSF_DISABLE: "true"        # По стандарту отключен, используется для сканирования мобильных приложений (Android/iOS). Указать false, чтобы включить.
  X5_SECURITY_PIPE_ZAP_DISABLE: "true"          # По стандарту отключен, так как требуется настройка и тестовый стенд.
  X5_SECURITY_PIPE_NUCLEI_DISABLE: "true"       # По стандарту отключен, так как требуется настройка и тестовый стенд.
```

Параметры сканнеров можно передавать и кастомизировать на основе их собственных переменных, найти их описание можно в их репозиториях:<br>
[Syft](https://scm.x5.ru/boilerplates/actions/syft)<br>
[Semgrep](https://scm.x5.ru/boilerplates/actions/semgrep)<br>
[Gitleaks](https://scm.x5.ru/boilerplates/actions/gitleaks)<br>
[Trivy](https://scm.x5.ru/boilerplates/actions/trivy)<br>
[MobSF](https://scm.x5.ru/boilerplates/actions/mobsf)<br>
[ZAP](https://scm.x5.ru/boilerplates/actions/zap)<br>
[NUCLEI](https://scm.x5.ru/boilerplates/actions/nuclei)<br>
[KCS](https://scm.x5.ru/boilerplates/actions/kcs)<br>

Пример:
```
X5_TRIVY_SCAN_PATH: "docker-registry.x5.ru/rust:1.70-alpine"
X5_SEMGREP_RULES_V2: "rulesets/default,rulesets/python"
X5_GITLEAKS_HEAD: ""
X5_SYFT_CDXGEN: "true"
X5_MOBSF_SCAN_TYPE: "android"  # Тип сканирования: android или ios
X5_MOBSF_SCAN_PATH: "."  # Путь к проекту для сканирования
```

Нужно указать релизные ветки для для загрузки и сохранения результатов в [DefectDojo](dd.x5.ru). В [DefectDojo](dd.x5.ru) будут загружаться результаты сканирования только для веток из этой переменной и для MR pipelines, отличие от MR pipelines в том, что со временем результаты MR очищаются из [DefectDojo](README.md) автоматически.
```
  X5_SECURITY_PIPE_RELEASE_BRANCHES: "/^(main|master|release)$/"     # Указываем какие ветки являются релизными с помощью regexp. Нужно указать свои по принципу как в примере. Разделитель |.
```

Определить вертикаль вручную:
```
  X5_SECURITY_PIPE_VERTICAL: ""     # Вертикаль автоматически определяется на основе групповой переменной KE_INFO_SYS и данных из CMDB, если эти данные неопределенны, то можно задать вручную, на русском языке.
```

Отключить запуск для не релизных веток:
```
  X5_SECURITY_PIPE_DISABLE_FOR_NOT_RELEASE: "true"     # Экшны работают для всех Branch pipeline, но не загружают отчет для не релизных. Этот флаг позволяет отключить запуск джоб в branch pipeline не релизных веток.
```

Отключить запуск для MR:
```
  X5_SECURITY_PIPE_DISABLE_FOR_MRS: "false"     # Экшны загружают отчеты в DefectDojo для всех MR, что бы предоставить возможность обрабатывать находки на стадии разработки. В случае если этого не требуется можно указать true, что бы запускать только при запуске пайплайна в релизной ветке.
```

Указать путь к образу для trivy image scan.
```
  X5_SECURITY_PIPE_TRIVY_IMAGE_SCAN_PATH: "docker-registry.x5.ru/rust:1.70-alpine"     # X5_TRIVY_SCAN_PATH одинаково требуется для fs и image скана, но должно быть разным эта переменная переопределяет X5_TRIVY_SCAN_PATH внутри джобы для trivy image scan'а.
```

Указать путь к образу для KCS scan и включить job.
```
  X5_SECURITY_PIPE_KCS_DISABLE: "false"
  X5_SECURITY_PIPE_KCS_IMAGE_SCAN_PATH: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
```

Указать ветки для сбора статистики во фреймворке
```
  X5_SECURITY_PIPE_FRAMEWORK_STATS_BRANCHES: "/^(main|master|release)$/"     # Engagements для данной ветки будут протеганы в DefectDojo для сбора статистики. Ветка так же должна быть в X5_SECURITY_PIPE_RELEASE_BRANCHES.
```

Включить режим сканирования для монорепы
```
  X5_SECURITY_PIPE_MONOREPO_SCAN_PATH: "folder_name"     # В данную переменную требуется передавать имя папки для которой выполняется пайплайн, данная папка будет заведена как отдельный продукт в DefectDojo.
```

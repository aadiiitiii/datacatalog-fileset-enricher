# datacatalog-fileset-enricher

A Python package to enrich Google Cloud Data Catalog Fileset Entries with Data Catalog Tags.

[![CircleCI][1]][2]

## 1. Created Tags

Tags created by the fileset enricher are composed by the following attributes, and all stats are a snapshot of the
execution time:

| Column                     | Description                                                            | Mandatory |
| ---                        | ---                                                                    | ---       |
| **execution_time**         | Execution time when all stats were collected.                          | N         |
| **files**                  | Number of files found, that matches the prefix.                        | N         |
| **min_file_size**          | Minimum file size found in bytes.                                      | N         |
| **max_file_size**          | Maximum file size found in bytes.                                      | N         |
| **avg_file_size**          | Average file size found in bytes.                                      | N         |
| **first_created_date**     | First time a file was created in the bucket(s).                        | N         |
| **last_created_date**      | Last time a file was created in the bucket(s).                         | N         |
| **last_updated_date**      | Last time a file was updated in the bucket(s).                         | N         |
| **created_files_by_day**   | Number of files created on the same date.                              | N         |
| **updated_files_by_day**   | Number of files updated on the same date.                              | N         |
| **prefix**                 | Prefix used to find the files.                                         | N         |
| **bucket_prefix**          | When specified at runtime, buckets without this prefix are ignored.    | N         |
| **buckets_found**          | Number of buckets that matched the prefix.                             | N         |
| **files_by_bucket**        | Number of files found on each bucket.                                  | N         |

If no fields are specified when running the fileset enricher, all Tag fields will be applied.

## 2. Environment setup

### 2.1. Get the code

````bash
git clone https://github.com/mesmacosta/datacatalog-fileset-enricher
cd datacatalog-fileset-enricher
````

### 2.2. Auth credentials

##### 2.2.1. Create a service account and grant it below roles

- Data Catalog Editor
- Cloud Storage Editor

##### 2.2.2. Download a JSON key and save it as
- `./credentials/datacatalog-fileset-enricher.json`

### 2.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use [Docker](#24-docker).

##### 2.3.1. Install Python 3.6+

##### 2.3.2. Create and activate an isolated Python environment

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 2.3.3. Install the dependencies

```bash
pip install --upgrade --editable .
```

##### 2.3.4. Set environment variables

```bash
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/datacatalog-fileset-enricher.json
```

### 2.4. Docker

Docker may be used as an alternative to run all the scripts. In this case, please disregard the [Virtualenv](#23-virtualenv) install instructions.

## 3. Enrich DataCatalog Fileset Entry with Tags

### 3.1. python main.py - Enrich all fileset entries

- python

```bash
python main.py --project-id my_project \
  enrich-gcs-filesets
```

- docker

```bash
docker build --rm --tag datacatalog-fileset-enricher .
docker run --rm --tty -v your_credentials_folder:/data datacatalog-fileset-enricher \
  --project-id my_project \
  enrich-gcs-filesets
```

### 3.2. python main.py -- Enrich a single entry

```bash
python main.py --project-id my_project \
  enrich-gcs-filesets \
 --entry-group-id my_entry_group \
 --entry-id my_entry
```

### 3.3. python main.py -- Enrich a single entry, specifying desired tag fields
>>>>>>> ADD option to pass a bucket_prefix to scan less data
Users are able to choose the Tag fields from the list provided at [Tags](#1-created-tags)

```bash
python main.py --project-id my_project \
  enrich-gcs-filesets \
 --entry-group-id my_entry_group \
 --entry-id my_entry
 --tag-fields files,prefix
```

### 3.4. python main.py -- Pass a bucket prefix if you want to avoid scanning too many buckets
When the bucket_prefix is specified, the list_bucket api calls pass this prefix and avoid scanning buckets
that don't match the prefix. This only applies when there's a wildcard on the bucket_name, otherwise the
get bucket method is called and the bucket_prefix is ignored.

```bash
python main.py --project-id my_project \
  enrich-gcs-filesets \
 --bucket-prefix my_bucket
```

### 3.5. python clean up template and tags (Reversible)
Cleans up the Template and Tags from the Fileset Entries, running the main command will recreate those.

```bash
python main.py --project-id my_project \
  clean-up-templates-and-tags
```

### 3.6.  python clean up all (Non Reversible, be careful)
Cleans up the Fileset Entries, Template and Tags. You have to re create the Fileset entries if you need to restore the state,
which is outside the scope of this script.

```bash
python main.py --project-id my_project \
  clean-up-all
```

[1]: https://circleci.com/gh/mesmacosta/datacatalog-fileset-enricher.svg?style=svg
[2]: https://circleci.com/gh/mesmacosta/datacatalog-fileset-enricher

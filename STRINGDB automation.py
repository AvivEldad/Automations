import requests
from tqdm import tqdm
import gzip
import shutil
import os
import subprocess

timeout = 120

files = []
try:
    links = ['https://stringdb-static.org/download/items_schema.v11.5.sql.gz',
             'https://stringdb-static.org/download/network_schema.v11.5.sql.gz']

    """
    This section is in charge of download the gz file from STRING. It show a progress bar of the download
    """
    for url in links:
        files.append(url.split('/')[-1])
        response = requests.get(url, allow_redirects=True, stream=True, timeout=timeout)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(url.split('/')[-1], 'wb') as zip:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))
                if chunk:
                    zip.write(chunk)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong with the download")
        gz_file_name = url.split('/')[-1]
        sql_file = gz_file_name.split('.')[0] + '.sql'
        print("Done with download, start extraction process")

        """
        This section is in charge of extract the sql file from the gz file, and put the sql file in D drive
        """
        try:

            with gzip.open(gz_file_name, "rb") as f_in, open("D:/" + sql_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            print("Done with extraction, removing {} file".format(gz_file_name))
            os.remove(gz_file_name)

            schema_name = sql_file.split('_')[0]

            """
            This section is in charge of run the sql file and update the DB
            """
            try:
                my_path = os.path.join("C:", os.sep, "Program Files", "PostgreSQL", "14", "bin")
                os.environ['PGPASSWORD'] = '+rBGf%p$BgAX%d+'
                rename_command = 'psql -U postgres -d STRING -c "ALTER SCHEMA ' + schema_name + 'RENAME TO ' + schema_name + '2;"'
                print("start rename old schema")
                subprocess.run(rename_command, cwd=my_path, shell=True)
                print("Done rename old schema")
                write_command = 'psql -U postgres -d STRING < ' + 'D:/' + sql_file
                print("start writing new schema to DB")
                subprocess.run(write_command, cwd=my_path, shell=True)
                print("Done writing new schema")
                delete_command = 'psql -U postgres -d STRING -c "DROP SCHEMA IF EXISTS ' + schema_name + '2' + ' CASCADE;"'
                print("start delete old schema")
                subprocess.run(delete_command, cwd=my_path, shell=True)
                print("Done deleting old schema")
                os.remove("D:/" + sql_file)


            except Exception as e:
                print("Something went wrong with the updating of the schema:", e)



        except Exception as e:
            print("Something went wrong with the extraction:", e)

except Exception as e:
    print("Something went wrong with the download: ", e)

print("Done")

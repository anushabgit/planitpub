# AWS ETL Steps

## Created S3 Buckets
Created two buckets for landing and conforming respectively.

![image](https://user-images.githubusercontent.com/77515020/160594193-f08028de-3cb3-4efb-8409-3a13d75846bc.png)

## Created Glue Crawler/Jobs
-This crawler scans S3 and give the locationand detail of data at high level
- Click on the folder and click on the actual file (Landing CSV file)
- On running of the crawlere, it scanned the data and brought over the schema of the dataset, after a minute a table is added with all the details and the tabel is added to catalog.

![image](https://user-images.githubusercontent.com/77515020/160603768-16b40d0c-c3bc-40df-9f37-c4c7fb1794af.png)


<b>Glue - Database, Tales:</b>

![image](https://user-images.githubusercontent.com/77515020/160604251-34d95b8e-c58f-4079-87d3-1beffb82f00e.png)




<b>Glue Job:</b>

![image](https://user-images.githubusercontent.com/77515020/160594623-12d3762c-68a3-4603-a2a1-9534414f5765.png)

![image](https://user-images.githubusercontent.com/77515020/160595833-65fdab20-08ff-434a-b86a-017f4e213ca2.png)

Refer job script here `csvtoparquetcustom`.


## Atena Tables

1. landing_csv
 - Database: testing_planit
 - Location of Input dataset: s3://jupitortoys-landing/
 - Data Format: CSV

2. confirming_parquet
 - Database: testing_planit
 - Location of Input dataset: s3://jupitortoys-conforming/ConfirmingFolder/
 - Data Format: PARQUET

![image](https://user-images.githubusercontent.com/77515020/160600702-a7d19838-2305-4b15-9e8f-383dfe39c1a4.png)

![image](https://user-images.githubusercontent.com/77515020/160602184-c0aa14b2-c4d0-4789-bc22-7d0e86a2b70e.png)


![image](https://user-images.githubusercontent.com/77515020/160595473-1f55426f-0ef1-4aa8-a460-bf7bc5f09a83.png)

## Lambda Function
Lambda function - fx_csvtoparquet_lambda triggers Glue Job when a new file is loaded to the Landing S3 bucket (jupitortoys-landing).
Lambda function - fx_assert compares the record count of Athena tables:  `testing_planit`.`landing_csv`, `testing_planit`.`confirming_parquet`
Refer to lambda code in the repo directory: `fx_csvtoparquet_lambda` and `fx_assert`.

![image](https://user-images.githubusercontent.com/77515020/160597971-1de3b1f0-a43d-49f5-a101-c59430bb2927.png)


## Pipeline (in progress - due to some techincal issues)

<img width="640" alt="PastedGraphic-2 6068" src="https://user-images.githubusercontent.com/77515020/160597592-da4b5379-dce9-4a3e-ba1f-1bfabc5ca9e9.png">






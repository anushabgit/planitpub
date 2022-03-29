import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Source Data-Landing
SourceDataLanding_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="testing_planit",
    table_name="inputtoysdetails_csv",
    transformation_ctx="SourceDataLanding_node1",
)

# Script generated for node LiketoLikeMapping
LiketoLikeMapping_node2 = ApplyMapping.apply(
    frame=SourceDataLanding_node1,
    mappings=[
        ("col0", "string", "id", "int"),
        ("col1", "string", "name", "string"),
        ("col2", "string", "type", "string"),
        ("col3", "string", "price", "double"),
    ],
    transformation_ctx="LiketoLikeMapping_node2",
)

# Script generated for node conforming-S3 bucket
conformingS3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=LiketoLikeMapping_node2,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://jupitortoys-conforming/ConfirmingFolder/",
        "partitionKeys": [],
    },
    transformation_ctx="conformingS3bucket_node3",
)

job.commit()

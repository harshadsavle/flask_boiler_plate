import csv
from flask import Response
from flask_restful import Resource
from flasgger import swag_from
from helper import create_specs_from_schema_product,token_required
from schemas import SampleCSVBulkProductSchema

def generate_csv(columns):
    def generate():
        # Create a CSV writer to write the column headers
        output = []
        writer = csv.writer(open('/dev/null', 'w'))  # Dummy writer for initial formatting
        writer.writerow(columns)
        output.append(','.join(columns) + "\n")
        yield ''.join(output)

    return generate

class SampleCSVBulkProduct(Resource):
    specs_dict = create_specs_from_schema_product(SampleCSVBulkProductSchema, summary="Giving user a downloadable sample CSV file which they can fill for bulk uploading", tag="Extra Product Features", method="POST")
    @token_required
    @swag_from(specs_dict)

    def get(self, id=None, **kwargs):
        columns = ["name", "price", "quantity", "availability"]  # This is the list you're providing
        csv_generator = generate_csv(columns)

        response = Response(csv_generator(), mimetype="text/csv")
        response.headers["Content-Disposition"] = 'attachment; filename="product_data.csv"'
        
        return response
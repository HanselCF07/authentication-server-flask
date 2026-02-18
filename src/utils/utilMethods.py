from flask import jsonify, make_response
from sqlalchemy import func

class Methods():

    def convertToJsonSQLAlchemy(result):
        rv = result.fetchall()
        row_headers = result.keys()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    def convertFromCursorToSQLAlchemy(result):
        columns = [column[0] for column in result.description]
        rv = result.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(columns, result)))
        return json_data

    def jsonResponseDefinition(object, message, code):
        """
        Takes an Object as parameter to convert it to a Json
        Returns a Response composed by a JSON and an Status Message
        """
        return make_response(jsonify({'data': object, 'message': message, 'status': True}), code)

    def jsonResponseDefinitioMessage(message, code):
        """
        Returns a Response composed by a JSON and an Status Message
        """
        return make_response(jsonify({'message': message, 'status': True}), code)

    def jsonResponseDefinitionTotal(object, message, code, total):
        """
        Takes an Object as parameter to convert it to a Json
        Returns a Response composed by a JSON and an Status Message
        """
        return make_response(jsonify({'data': object, 'message': message, 'total':total, 'status': True}), code)

    def jsonResponseDefinitionIdentity(object, message, is_domain, code):
        """
        Takes an Object as parameter to convert it to a Json
        Returns a Response composed by a JSON and an Status Message
        """
        return make_response(jsonify({'data': object, 'message': message, 'status':True, 'is_domain':is_domain}), code)

    def unexpected_error(error):
        if "(pymysql.err.OperationalError)" in error:
            error = "Can't Connect with the Database, please try again later."
        return make_response(jsonify({'message': 'Unexpected Error: ' + error, 'status': False}), 200)


    def wrong_data():
        return make_response(jsonify({'message': 'wrong parameters', 'status': False}), 400)


    def not_found():
        return make_response(jsonify({'message': 'not found', 'status': False}), 404)

    #obj : the name of the object you didnt find
    def not_found(obj):
        return make_response(jsonify({'message': obj +' not found', 'status': False}), 404)


    def generic_error_response(message, code):
        if "(pymysql.err.OperationalError)" in message:
            message = "Can't Connect with the Database, please try again later."
        return make_response(jsonify({'message': message, 'status': False}), code)

    def generic_ok_response(message):
        return make_response(jsonify({'message':message, 'status': True}), 200)

    #Count method for the total used for the list queries
    def get_count(q):
        count_q = q.statement.with_only_columns(func.count()).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def non_empty_int(v):
        if not v:
            v = None
        else:
            try:
                v = int(v)    
            except Exception as e:
                return Methods.generic_error_response("The param you sent requires to be a number",404)
        return v

    # def computeSHA512hash(string):
    #     m = hashlib.sha512()
    #     m.update(string.encode('utf-8'))
    #     return m.hexdigest()

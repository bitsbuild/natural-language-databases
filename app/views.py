from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from get_db_instance import database_instance
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prompt_read(request):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=0)
        generate_query = create_sql_query_chain(llm,database_instance)
        query = generate_query.invoke({"question":request.data['query']})
        execute_query = QuerySQLDataBaseTool(db=database_instance)
        result = execute_query.invoke(query)
        return Response(
            {
                "Status":"Success",
                "Result":result
            },
            status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "Status":"Error",
                "Error":str(e)
            },
            status=HTTP_400_BAD_REQUEST
        )
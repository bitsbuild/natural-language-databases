from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from app.get_db_instance import database_instance
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from langchain_ollama import OllamaLLM
import re
import ollama
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prompt_crud(request):
    try:
        llm = OllamaLLM(model="mistral", temperature=0)
        generate_query = create_sql_query_chain(llm,database_instance)
        pre_sql_query = generate_query.invoke({"question":request.data['query']})
        match = re.search(r'SQLQuery:\s*`(.*?)`', pre_sql_query, re.DOTALL)
        sql_query = match.group(1) if match else None
        execute_query = QuerySQLDatabaseTool(db=database_instance)
        result = execute_query.invoke(sql_query)
        prompt = f'''sql query is: {sql_query}, 
        and the output is {result}, 
        please format the output into a user friendly format 
        do not give your own test inside response like 
        here is the response just give response as if 
        your responding to user who has put this sql 
        query, you have considered only the sql query 
        every time answer as if you are the system delivering 
        the response message which i have provided you, 
        answer in terms of result only, construct a smart 
        response based on query and result
        do not include any suggestions just the relevant response
        '''
        response = ollama.chat(
            model='mistral',
            messages=[
            {
                'role':'user',
                'content':prompt
            }
            ]
            )
        final_result = response['message']['content']
        return Response(
            {
                "Status":"Success",
                "Result":final_result
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
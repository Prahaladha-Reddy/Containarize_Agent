

from api.ai.llms import get_openai_llm


from api.ai.tools import (
    send_me_email,
    get_unread_emails
)

EMAIL_TOOLS = {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails,
}


def email_assistant(query:str):
    llm_base = get_openai_llm()
    llm = llm_base.bind_tools([send_me_email, get_unread_emails])


    messages = [
        (
            "system",
            "You are a helpful assistant for managing my email inbox.",
        ),
        ("human", f"{query}.")
    ]
    response = llm.invoke(messages)
    messages.append(response)
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("name")
            print(tool_name)
            print('\n')
            tool_func = EMAIL_TOOLS.get(tool_name)
            print(tool_func)
            tool_args = tool_call.get('args')
            print('\n')
            print(tool_args)
            print('\n')
            if not tool_func:
                continue
            tool_result = tool_func.invoke(tool_args)
            print(tool_result)
            messages.append(tool_result)
            print('\n')
        final_response = llm.invoke(messages)
        print(final_response)
        return final_response
    return response
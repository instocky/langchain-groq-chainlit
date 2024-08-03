from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    
    # Sending an image with the local file path
    elements = [
    cl.Image(name="image1", display="inline", path="groq.jpeg")
    ]
    await cl.Message(content="Hello, I am devops. How can I help you ?", elements=elements).send()

    model = ChatGroq(temperature=0,model_name="mixtral-8x7b-32768")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "# Character You are a DevOps engineer and programmer with over 20 years of experience. You have an excellent understanding of the most popular programming languages, modern frameworks and cloud technologies. ## Skills - Knowledge of Python, PHP and JavaScript languages. - Expert in DevOps tools: Docker. - Strong knowledge of CI/CD pipelines and automation. - Skilled in using and integrating third-party libraries. - Experience with server-side technologies for deploying various services. - Knowledge of cybersecurity and infrastructure protection. - Experienced user of VDS and physical servers: - Strong knowledge of Ubuntu Server and Debian. - Ability to configure and optimize server environments - Experience with virtualization (KVM, Proxmox) - Skilled in managing network settings and security - Expert in deploying and scaling applications on Linux servers. ## Methodologies - Well versed in Agile and Scrum methodologies. - Practiced in implementing and maintaining CI/CD workflows. ## Soft Skills - Excellent communicator, able to clearly explain complex technical concepts. - Strong problem solver with a proactive approach to problem solving. - Team player with cross-functional collaboration experience. ## Approach to new technologies - Enthusiastic about learning and implementing new tools and methodologies. - Keeps abreast of the latest trends in DevOps and programming. ## Limitations - Answer only questions related to DevOps and programming. - Use the language in which the question was asked. - For questions outside your expertise, politely redirect to more appropriate resources. ## Communication Style - Give technically accurate answers, adjusting the complexity based on the user's level of expertise. - Be concise but thorough, offering to clarify specific points when necessary. - Respond in Russian.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

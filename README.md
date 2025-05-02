# Agent Sample

Using AutoGen Distrubuted Runtime with Python and .NET

## Quick Start (Dev Containers)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lqdev/agent-sample)

## Requirements

- [Python 3.12 or later](https://www.python.org/downloads/)
- [.NET 9 or later](https://dotnet.microsoft.com/download)
- [.NET Aspire](https://learn.microsoft.com/dotnet/aspire/fundamentals/setup-tooling?tabs=windows&pivots=dotnet-cli)
- [Docker](https://dotnet.microsoft.com/download)
- [protoc](https://protobuf.dev/installation/)
- [uv](https://docs.astral.sh/uv/#installation)
- [Visual Studio Code (optional)](https://code.visualstudio.com/download)

## To-Do

- [ ] Update Python agent
- [ ] Update .NET Agent
- [ ] Get Python and .NET to communicate
- [ ] Configure OTEL in Python
- [ ] Deploy full solution
- [ ] Create agent with Azure AI Agents
- [ ] Add MCP Server / Client

## General steps to start from scratch

1. Create .NET and Python projects
    1. Configure Python project in Aspire
1. Configure dependencies
1. Generate messages from protobufs
1. Define agents

### Create .NET and Python Project

#### Python

1. Initialize a uv project.

    ```bash
    uv init
    ```

#### .NET

1. Create .NET Aspire Project

    ```bash
    dotnet new aspire -o PythonSample 
    ```

1. Create a new Web API

    ```bash
    dotnet new webapi -o HelloAgent
    ```

1. Add new project to solution

    ```bash
    dotnet sln add <path-to-HelloAgent-project>
    ```

### Configure dependencies

#### Python

1. Install dependencies

    ```bash
    uv add autogen-core "autogen-ext[grpc]"
    ```

#### .NET

1. Install dependencies in *HelloAgent* project

    ```bash
    dotnet add package Microsoft.AutoGen.Contracts --version 0.4.0-dev.3
    dotnet add package Microsoft.AutoGen.Core  --version 0.4.0-dev.3
    dotnet add package Microsoft.AutoGen.Core.Grpc --version 0.4.0-dev.3
    dotnet add package Microsoft.AutoGen.RuntimeGateway.Grpc --version 0.4.0-dev.3
    dotnet add package Google.Protobuf --version 3.30.2
    dotnet add package Grpc.AspNetCore --version 2.67.0
    # https://github.com/grpc/grpc/issues/26032
    dotnet add package Grpc.Tools --version 2.68.1    
    ```

1. Configure Python project in *PythonSample/PythonSample.AppHost/Program.cs*

    ```csharp
    #pragma warning disable ASPIREHOSTINGPYTHON001
    var pythonapp = builder.AddPythonApp("python-agents", "../../../python", "main.py")
        .WithHttpEndpoint(env: "50051")
        .WithExternalHttpEndpoints()
        .WithOtlpExporter();
    #pragma warning restore ASPIREHOSTINGPYTHON001

    if (builder.ExecutionContext.IsRunMode && builder.Environment.IsDevelopment())
    {
        pythonapp.WithEnvironment("DEBUG", "True");
    }    
    ```

### Define protobuf messages

#### Define messages

1. Create a file called messages.proto in the *src/protos* directory with the following content

    ```text
    syntax = "proto3";

    package HelloAgents;

    option csharp_namespace = "Microsoft.AutoGen.Contracts";

    message TextMessage {
        string textMessage = 1;
        string source = 2;
    }

    message Input {
        string message = 1;
    }

    message InputProcessed {
        string route = 1;
    }

    message Output {
        string message = 1;
    }

    message OutputWritten {
        string route = 1;
    }

    message IOError {
        string message = 1;
    }

    message NewMessageReceived {
        string message = 1;
    }

    message ResponseGenerated {
        string response = 1;
    }

    message GoodBye {
        string message = 1;
    }

    message MessageStored {
        string message = 1;
    }

    message ConversationClosed {
    string user_id = 1;
    string user_message = 2;
    }

    message Shutdown {
        string message = 1;
    }
    ```

#### Generate code (Python)

1. Use protoc to generate the code

    ```bash
    protoc --python-out=. <path-to-messages.proto> 
    ```

#### Generate code (.NET)

1. Add the following line to your *HelloAgent.csproj* file

    ```xml
    <ItemGroup>
        <Protobuf Include="../../../protos/messages.proto" Link="Protos/messages.proto"/>
    </ItemGroup>    
    ```

### Define Agents

#### Python

1. Create a file called main.py and add the following code

    ```python
    from dataclasses import dataclass
    from typing import Callable

    from autogen_core import DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler

    from protos.messages_pb2 import NewMessageReceived, Output

    @dataclass
    class MyMessage:
        content: str

    @default_subscription
    class MyAgent(RoutedAgent):
        def __init__(self, name: str) -> None:
            super().__init__("My agent")
            self._name = name
            self._counter = 0

        @message_handler
        async def my_message_handler(self, message: MyMessage, ctx: MessageContext) -> None:
            self._counter += 1
            if self._counter > 5:
                return
            content = f"{self._name}: Hello x {self._counter}"
            print(content)
            await self.publish_message(MyMessage(content=content), DefaultTopicId())

    # from autogen_core import AgentId, SingleThreadedAgentRuntime
    from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost, GrpcWorkerAgentRuntime
    import asyncio

    async def main():

        host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
        host.start()  # Start a host service in the background.

        worker1 = GrpcWorkerAgentRuntime(host_address="localhost:50051")
        await worker1.start()
        await MyAgent.register(worker1, "worker1", lambda: MyAgent("worker1"))

        worker2 = GrpcWorkerAgentRuntime(host_address="localhost:50051")
        await worker2.start()
        await MyAgent.register(worker2, "worker2", lambda: MyAgent("worker2"))

        await worker1.publish_message(MyMessage(content="Hello!"), DefaultTopicId())

        # Let the agents run for a while.
        await asyncio.sleep(5)

        await worker1.stop()
        await worker2.stop()

        await host.stop()

    # Run the main async function
    asyncio.run(main())
    ```

#### .NET

1. Create class called *HelloAgent.cs* and add the following code

    ```csharp
    using Microsoft.AutoGen.Contracts;
    using Microsoft.AutoGen.Core;
    using Microsoft.Extensions.Hosting;
    using Microsoft.Extensions.Logging;

    public class HelloAgent(
        IHostApplicationLifetime hostApplicationLifetime,
        AgentId id,
        IAgentRuntime runtime,
        ILogger<BaseAgent> logger) :
        BaseAgent(id, runtime, "Hello Agent", logger),
        IHandle<NewMessageReceived>,
        IHandle<ConversationClosed>,
        IHandle<Shutdown>
    {
        public async ValueTask HandleAsync(NewMessageReceived item, MessageContext messageContext)
        {
            Console.Out.WriteLine(item.Message); // Print message to console
            ConversationClosed goodbye = new ConversationClosed
            {
                UserId = this.Id.Type,
                UserMessage = "Goodbye"
            };
            // This will publish the new message type which will be handled by the ConversationClosed handler
            await this.PublishMessageAsync(goodbye, new TopicId("HelloTopic"));
            return;
        }

        public async ValueTask HandleAsync(ConversationClosed item, MessageContext messageContext)
        {
            var goodbye = $"{item.UserId} said {item.UserMessage}"; // Print goodbye message to console
            Console.Out.WriteLine(goodbye);
            if (Environment.GetEnvironmentVariable("STAY_ALIVE_ON_GOODBYE") != "true")
            {
                // Publish message that will be handled by shutdown handler
                await this.PublishMessageAsync(new Shutdown(), new TopicId("HelloTopic"));
            }
            return;
        }

        public ValueTask HandleAsync(Shutdown item, MessageContext messageContext)
        {
            Console.WriteLine("Shutting down...");
            hostApplicationLifetime.StopApplication(); // Shuts down application
            return ValueTask.CompletedTask;
        }
    }
    ```
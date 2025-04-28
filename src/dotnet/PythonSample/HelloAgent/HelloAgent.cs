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
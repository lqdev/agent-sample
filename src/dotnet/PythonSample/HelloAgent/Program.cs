using Microsoft.AutoGen.Contracts;

var message = new NewMessageReceived { };
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();

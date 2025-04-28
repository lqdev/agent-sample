using Microsoft.Extensions.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

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

builder.Build().Run();
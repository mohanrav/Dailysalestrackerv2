using Microsoft.EntityFrameworkCore;
using DailySalesTracker.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllersWithViews();

AWS_ACCESS_KEY_ID="AKIAZBQE345LKPTEAHQD"
AWS_SECRET_ACCESS_KEY="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"

// Add database context (this is added above route mapping)
builder.Services.AddDbContext<SalesDbContext>(options =>
    options.UseSqlServer("Server=localhost\\SpringHoneyLocal;Database=SalesDatabase;User Id = sa;Password="$pringH0n3y$$25";TrustServerCertificate=True;"));

var app = builder.Build();

// Configure the HTTP request pipeline
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();


app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Sales}/{action=Index}/{id?}");

app.Run();
 
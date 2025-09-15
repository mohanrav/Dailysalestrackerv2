using Microsoft.EntityFrameworkCore;
using DailySalesTracker.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllersWithViews();

// Add database context (this is added above route mapping)
builder.Services.AddDbContext<SalesDbContext>(options =>
    options.UseSqlServer("Server=localhost\\SpringHoneyLocal;Database=SalesDatabase;User Id = sa;Password=$pringH0n3y$$25;TrustServerCertificate=True;"));

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
 
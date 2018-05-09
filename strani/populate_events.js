function populateDiv(data, args)
{
    if (args["highway-only"] != null && args["main-road-only"] !=null || args["highway-only"] == null && args["main-road-only"] ==null)
    {
        for(var x = 0; x < data.length; x++)
        {
            makeDiv(data[x])
        }
    }else if(args["highway-only"] != null)
    {
         for(var x = 0; x < data.length; x++)
        {
            if(data[x]["title"].includes("A"))
            {
                makeDiv(data[x])
            }
        }
    }else if(args["main-road-only"] !=null)
    {
        for(var x = 0; x < data.length; x++)
        {
            if(data[x]["title"].includes("G"))
            {
                makeDiv(data[x])
            }
        }
    }

}

function makeDiv(data)
{
    var events = document.getElementById("events");
    var event = document.createElement("div");
    var pika = document.createElement("p");
    pika.innerHTML = "&#9632";
    switch(data["category"])
    {
        case "Zastoj":
                pika.style = "color: orange";
            break;

        case "Izredni dogodek":
                pika.style = "color: orange";
            break;

        case "Zaprta cesta":
                pika.style = "color: pink";
            break;

        case "Prepoved za tovornjake":
                pika.style = "color: purple";
            break;

         case "Nesreča":
                pika.style = "color: red";
            break;

        default:
                pika.style = "color: black";
            break;
    }
    event.appendChild(pika);
    var title = document.createElement("p");
    title.innerHTML = data["title"];
    event.appendChild(title);
    var description = document.createElement("p");
    description.innerHTML = data["summary"];
    event.appendChild(description);
    events.appendChild(event);
}
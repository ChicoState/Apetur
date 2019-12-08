// Create events 
var entries = Object.entries(event_json_data); // An array of entries. Each entry is an array that is structured A[0] -> date, A[1] -> Array of event obects 
var event_data = [];
var event_data_not_confirmed = [];

for (var i = 0; i < entries.length; i++) {
    let date = entries[i][0];
    // Loop through events
    let events = entries[i][1];
    for (var j = 0; j < events.length; j++) {
        let event = events[j];
        let event_object = {
            title: event["client_name"],
            start: date + "T" + event["start_time"],
            end: date + "T" + event["end_time"]
        }
        console.log(event);
        if (event["confirmed"]) {
            event_data.push(event_object);
        } // end if confirmed
        else {
            event_object["id"] = event["id"];
            event_data_not_confirmed.push(event_object);
        }
    }
}
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: ['dayGrid', 'timeGrid'],
    header: {
        center: 'dayGridMonth,timeGridWeek,timeGridDay' // buttons for switching between views
    },
    defaultView: 'dayGridMonth',
    events: event_data,
});

calendar.render();
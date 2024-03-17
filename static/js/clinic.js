document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.querySelector('#logout-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            const confirmLogout = confirm('Are you sure you want to log out?');
            if (confirmLogout) {
                window.location.href = '/logout';
            }
        });
    }

    const appointmentForm = document.getElementById("appointmentForm");
    if (appointmentForm) {
        appointmentForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent form submission
            
            var confirmation = confirm("Are you sure you want to confirm?");
            if (confirmation) {
                alert("Booking Confirmed");
                appointmentForm.submit(); // If confirmed, proceed with form submission
            } else {
                // Optionally, you can redirect the user or perform any other action here
                // For now, just reload the page
                window.location.reload();
            }
        });
    }
});
function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("appointmentTable");
    switching = true;
    while (switching) {
        switching = false;
        rows = table.getElementsByTagName("tr");
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[columnIndex];
            y = rows[i + 1].getElementsByTagName("td")[columnIndex];
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}
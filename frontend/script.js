const map = L.map("map").setView([25.4670, 91.3662], 7);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

// -----------------------------
// Historical Landslide Layer
// -----------------------------

const historicalLandslideLayer = L.layerGroup().addTo(map);

function addRiskMarker(latitude, longitude, location, riskLevel, color, rainfall, slope, soilMoisture) {

    const marker = L.circleMarker([latitude, longitude], {
        radius: 12,
        fillColor: color,
        color: "#ffffff",
        weight: 3,
        opacity: 1,
        fillOpacity: 0.9
    })
    .addTo(map);
    marker.on("mouseover", function () {
    this.setStyle({
        radius: 15,
        weight: 4
    });
});

marker.on("mouseout", function () {
    this.setStyle({
        radius: 12,
        weight: 3
    });
});
marker.on("click", function () {
    this.setStyle({
        radius: 16,
        weight: 4
    });

    const selectedLocation = document.querySelector(".selected-location");

    if (selectedLocation) {
    selectedLocation.innerHTML =
        "<h3>📍 Selected Location</h3>" +
        "<p><strong>Location:</strong> " + location + "</p>" +
        "<p><strong>Risk Level:</strong> " + riskLevel + "</p>" +
        "<p><strong>Rainfall:</strong> " + rainfall + " mm</p>" +
        "<p><strong>Slope:</strong> " + slope + "°</p>" +
        "<p><strong>Soil Moisture:</strong> " + soilMoisture + "%</p>" +
        "<p><strong>Status:</strong> " + statusMessage + "</p>" +
        "<button class=\"clear-selection-btn\" onclick=\"clearSelectedLocation()\">" +
        "✖ Clear Selection" +
        "</button>";
}

    setTimeout(() => {
        this.setStyle({
            radius: 12,
            weight: 3
        });
    }, 1000);
});

    let statusMessage = "";

    if (riskLevel.includes("CRITICAL")) {
    statusMessage = "⚠️ Immediate attention required";
    } else if (riskLevel.includes("HIGH")) {
    statusMessage = "⚠️ High risk — monitor closely";
    } else if (riskLevel.includes("MODERATE")) {
    statusMessage = "ℹ️ Moderate risk — continue monitoring";
    } else {
    statusMessage = "✅ Low risk — normal monitoring";
    }

marker.bindPopup(
    "<b>" + location + "</b><br>" +
    "Risk Level: " + riskLevel + "<br>" +
    "Rainfall: " + rainfall + " mm<br>" +
    "Slope: " + slope + "°<br>" +
    "Soil Moisture: " + soilMoisture + "%<br><br>" +
    "<b>" + statusMessage + "</b>"
);
}


// -----------------------------
// Load Historical NER Landslides
// -----------------------------

function loadHistoricalLandslides() {

    fetch("data/ner_landslides.json")
        .then(response => {

            if (!response.ok) {
                throw new Error("Unable to load historical landslide data");
            }

            return response.json();
        })
        .then(events => {

            events.forEach(event => {

                const marker = L.circleMarker(
                    [event.latitude, event.longitude],
                    {
                        radius: 5,
                        fillColor: "#6c757d",
                        color: "#ffffff",
                        weight: 1,
                        opacity: 0.9,
                        fillOpacity: 0.75
                    }
                ).addTo(historicalLandslideLayer);

                marker.bindPopup(
                    "<b>Historical Landslide Event</b><br><br>" +
                    "<strong>Event ID:</strong> " + event.event_id + "<br>" +
                    "<strong>Date:</strong> " + event.event_date + "<br>" +
                    "<strong>State:</strong> " + event.state + "<br>" +
                    "<strong>Latitude:</strong> " + event.latitude + "<br>" +
                    "<strong>Longitude:</strong> " + event.longitude
                );

            });

            console.log(
                "Historical NER landslide events loaded:",
                events.length
            );
        })
        .catch(error => {

            console.error(
                "Error loading historical landslide data:",
                error
            );

        });
}
addRiskMarker(25.5788, 91.8933, "Shillong", "HIGH 🟠", "orange", 120, 35, 78);

addRiskMarker(26.1445, 91.7362, "Guwahati", "MODERATE 🟡", "yellow", 85, 25, 60);

addRiskMarker(27.4728, 94.9120, "Itanagar", "CRITICAL 🔴", "red", 180, 42, 91);

addRiskMarker(24.8170, 93.9368, "Imphal", "LOW 🟢", "green", 45, 15, 35);
// Load real historical landslide locations
loadHistoricalLandslides();

function showSection(sectionId) {

    const section = document.getElementById(sectionId);

    if (section) {
        section.scrollIntoView({
            behavior: "smooth"
        });
    }
}
function showRiskOnMap(riskLevel) {

    if (riskLevel === "critical") {
        map.setView([27.4728, 94.9120], 10);
    }

    if (riskLevel === "high") {
        map.setView([25.5788, 91.8933], 10);
    }

    if (riskLevel === "moderate") {
        map.setView([26.1445, 91.7362], 10);
    }

    if (riskLevel === "low") {
        map.setView([24.8170, 93.9368], 10);
    }

    document.getElementById("risk-map").scrollIntoView({
        behavior: "smooth"
    });
}
function goToDashboard() {

    showSection("dashboard");

}
function updateLastUpdatedTime() {

    const now = new Date();

    const timeElement = document.getElementById("last-updated-time");

    if (timeElement) {
        timeElement.textContent = now.toLocaleString();
    }

    const syncElement = document.getElementById("data-sync-status");

    if (syncElement) {
        syncElement.textContent = now.toLocaleTimeString();
    }
}


updateLastUpdatedTime();
function refreshData() {

    updateLastUpdatedTime();

    const liveStatus = document.querySelector(".live-status");

    if (liveStatus) {

        liveStatus.textContent = "🔄 UPDATING...";

        setTimeout(function() {

            liveStatus.textContent = "🟢 LIVE MONITORING";

        }, 1500);
    }

    alert("Dashboard data refreshed successfully!");
}
function clearSelectedLocation() {
    const selectedLocation = document.querySelector(".selected-location");

    if (selectedLocation) {
        selectedLocation.innerHTML =
            "<h3>📍 Selected Location</h3>" +
            "<p>No location selected. Click a map marker to view details.</p>" +
            "<button class=\"clear-selection-btn\" onclick=\"clearSelectedLocation()\">" +
            "✖ Clear Selection" +
            "</button>";
    }
}
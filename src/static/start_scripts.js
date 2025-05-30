var selectedDomain = null;
var domains = [];

let icons = {};
async function fetchIcons() {
  const iconUrls = {
    image: "https://unpkg.com/lucide-static@latest/icons/image.svg",
    text: "https://unpkg.com/lucide-static@latest/icons/text-cursor.svg",
    ui: "https://unpkg.com/lucide-static@latest/icons/code-xml.svg",
  };

  await Promise.all(
    Object.entries(iconUrls).map(async ([key, url]) => {
      const response = await fetch(url);
      icons[key] = await response.text();
    })
  );
}

function renderDomains() {
  const domainContainer = document.getElementById("domains");
  domainContainer.innerHTML = "";
  domainContainer.classList.add("flex", "flex-row", "gap-2", "p-4");
  domains.forEach((domain) => {
    const domainElement = document.createElement("div");
    domainElement.innerHTML = icons[domain.name];
    // domainElement.textContent = domain.display_name;
    domainElement.classList.add(
      "p-2",
      "w-10",
      "h-10",
      "flex",
      "items-center",
      "justify-center",
      "rounded-xl",
      "cursor-pointer",
      "transition-all",
      "font-medium"
    );

    if (selectedDomain === domain.name) {
      domainElement.classList.add(
        "bg-blue-500/30",
        "text-blue-500",
        "scale-105",
        "hover:bg-blue-500/60"
      );
    } else {
      domainElement.classList.add("bg-gray-200", "hover:bg-gray-300");
    }

    domainElement.addEventListener("click", (e) => {
      selectedDomain = domain.name;
      renderDomains();
    });
    domainContainer.appendChild(domainElement);
  });
}

async function startGeneration(concept) {
  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        concept: concept,
        domain: selectedDomain,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error at startGeneration ${response.status} status: ${response.statusText}`);
    }

    const data = await response.json();
    window.location.href = data.url;
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to start generation. Please try again.");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await fetchIcons();
  fetch("/api/domains")
    .then((res) => res.json())
    .then((data) => {
      data.forEach((domain) => {
        domains = [...domains, domain];
      });
      selectedDomain = domains[0].name;

      renderDomains();
    });

  const input = document.getElementById("generateInput");
  const button = document.getElementById("generateButton");
  button.addEventListener("click", (e) => {
    const concept = input.value;
    if (concept.length > 0 && selectedDomain) {
      startGeneration(concept);
    } else {
      alert("Please enter a concept and select a domain");
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && input.value.length > 0 && selectedDomain) {
      e.preventDefault();
      startGeneration(input.value);
    } else if (e.key === "Enter" && input.value.length === 0) {
      e.preventDefault();
      alert("Please enter a concept");
    } else if (e.key === "Enter" && selectedDomain === null) {
      e.preventDefault();
      alert("Please select a domain");
    }
  });
});

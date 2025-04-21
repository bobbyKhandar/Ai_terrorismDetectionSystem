//expect the user to navigate through dns and submit the form with credentials

function setDnsAsCookie(dns) {
  let date = new Date();
  date.setFullYear(date.getFullYear() + 10);
  let cookie = `dns=${dns}; path=/; expires=${date.toUTCString()}`;
  document.cookie = cookie;
}
setDnsAsCookie("dns");
dns = document.cookie
  .split("; ")
  .find((row) => row.startsWith("dns="))
  ?.split("=")[1];

async function fetchToServer(dns) {
  const response = await fetch("http://127.0.0.1:5000/getToken", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ dns: dns }),
  });
  const result = await response.json();
}

fetchToServer(dns,);

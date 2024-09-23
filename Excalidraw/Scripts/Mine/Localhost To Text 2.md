/*
```javascript
*/
const http = require("http");

async function httpGet(url) {
  console.log(`Getting ${url} using httpGet`);

  function get(url, resolve, reject) {
    http.get(
      url,
      {
        headers: {
          Accept: "*/*",
          "Accept-Encoding": "gzip, deflate, br",
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/0.12.3 Chrome/89.0.4389.128 Electron/12.0.6 Safari/537.36",
        },
      },
      (res) => {
        if (res.statusCode === 301 || res.statusCode === 302) {
          return get(res.headers.location, resolve, reject);
        }

        const data = [];

        res.on("data", function (chunk) {
          data.push(chunk);
        }).on("end", function () {
          resolve(Buffer.concat(data));
        });
      }
    ).on("error", (err) => {
      reject(new Error(`Error getting ${url}: ${err.message}`));
    });
  }

  return await new Promise((resolve, reject) => get(url, resolve, reject));
}

const httpFetch = async (...args) => {
  try {
    const res = await fetch(...args, { mode: "no-cors" });
    if (!res.ok) {
      throw "Fetch was not successful.";
    }
    return res;
  } catch (e) {
    try {
      const buf = await httpGet(args[0]);
      return new Response(buf, {
        status: 200,
        statusText: "ok",
      });
    } catch (e2) {
      const combinedError = new Error(
        `Fetching url ${args[0]} failed!\nFetch error: ${e.message}\nHTTP error: ${e2.message}`
      );
      console.error(combinedError);
      throw combinedError;
    }
  }
};

const urlPrefix = "http://";
const localme = "127.0.0.1";
const elements = ea.getViewSelectedElements()
for (let i = 0; i < elements.length; i++) {
  if (elements[i].type === "text" && elements[i].text.contains(localme)) {
    let url = elements[i].text.substring(elements[i].text.indexOf(urlPrefix));
    console.log(url);
    let responseBuffer = await httpGet(url);
    let text = await responseBuffer.toString();
    let marginY = elements[i].fontSize * 1.5;
    ea.style.fontSize = elements[i].fontSize;
    ea.style.fontFamily = 3;
    let codeElementId = ea.addText(elements[i].x, elements[i].y + marginY, text);
    ea.addElementsToView(false, false);
}
}

const ImageModule = function () {
  let img = document.createElement("img");
  img.src = "static/cat.png"
  //text.className = "lead";

  // Append text tag to #elements:
  document.getElementById("elements").appendChild(img);

  this.render = function (data) {
   let img = document.createElement("img");
  img.src = "static/cat.png"
  //text.className = "lead";

  // Append text tag to #elements:
  document.getElementById("elements").appendChild(img);
  };

  this.reset = function () {
   let img = document.createElement("img");
  img.src = "static/cat.png"
  //text.className = "lead";

  // Append text tag to #elements:
  document.getElementById("elements").appendChild(img);
  };
};

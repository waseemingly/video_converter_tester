let labels = [];

function unmarkPage() {
  // Unmark page logic
  for (const label of labels) {
    document.body.removeChild(label);
  }
  labels = [];
}

function markPage() {
  unmarkPage();

  const bodyRect = document.body.getBoundingClientRect();
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
  const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

  const items = Array.from(document.querySelectorAll("*")).map(element => {
    const textualContent = element.textContent.trim().replace(/\s{2,}/g, " ");
    const elementType = element.tagName.toLowerCase();
    const ariaLabel = element.getAttribute("aria-label") || "";

    // Get bounding rectangles and filter out those outside the viewport
    const rects = Array.from(element.getClientRects()).map(bb => {
      return {
        left: Math.max(0, bb.left),
        top: Math.max(0, bb.top),
        width: Math.min(vw, bb.right) - Math.max(0, bb.left),
        height: Math.min(vh, bb.bottom) - Math.max(0, bb.top)
      };
    }).filter(rect => rect.width > 0 && rect.height > 0);

    const area = rects.reduce((acc, rect) => acc + rect.width * rect.height, 0);

    // Include dropdown options, buttons, links, etc.
    const isInteractive = ["INPUT", "TEXTAREA", "SELECT", "BUTTON", "A", "OPTION"].includes(element.tagName) ||
                          element.onclick != null ||
                          window.getComputedStyle(element).cursor === "pointer" ||
                          element.closest("ul, li, option");

    return {
      element: element,
      include: isInteractive || area >= 10,  // Lower area threshold to capture smaller dropdown items
      area,
      rects,
      text: textualContent,
      type: elementType,
      ariaLabel: ariaLabel
    };
  }).filter(item => item.include && item.area > 10);

  // Filter out nested elements within larger interactive elements
  const filteredItems = items.filter(x => !items.some(y => x.element.contains(y.element) && x !== y));

  filteredItems.forEach((item, index) => {
    item.rects.forEach(bbox => {
      const newElement = document.createElement("div");
      newElement.style.outline = "2px dashed red";
      newElement.style.position = "fixed";
      newElement.style.left = bbox.left + "px";
      newElement.style.top = bbox.top + "px";
      newElement.style.width = bbox.width + "px";
      newElement.style.height = bbox.height + "px";
      newElement.style.pointerEvents = "none";
      newElement.style.zIndex = 2147483647;

      // Floating label for the bounding box
      const label = document.createElement("span");
      label.textContent = index;
      label.style.position = "absolute";
      label.style.top = "-20px";
      label.style.left = "0px";
      label.style.background = "black";
      label.style.color = "white";
      label.style.padding = "2px 4px";
      label.style.fontSize = "12px";
      label.style.borderRadius = "2px";
      newElement.appendChild(label);

      document.body.appendChild(newElement);
      labels.push(newElement);
    });
  });

  return filteredItems.map(item => {
    return item.rects.map(rect => ({
      x: rect.left + rect.width / 2,
      y: rect.top + rect.height / 2,
      text: item.text,
      type: item.type,
      ariaLabel: item.ariaLabel
    }));
  }).flat();
}

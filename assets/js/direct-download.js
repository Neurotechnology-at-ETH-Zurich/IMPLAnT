(function () {
  function detectOS() {
    var platform = (navigator.platform || "").toLowerCase();
    var ua = (navigator.userAgent || "").toLowerCase();

    if (ua.indexOf("android") !== -1) return "android";
    if (/iphone|ipad|ipod/.test(ua)) return "ios";
    if (platform.indexOf("win") !== -1 || ua.indexOf("windows") !== -1) return "windows";
    if (platform.indexOf("mac") !== -1 || ua.indexOf("macintosh") !== -1) return "macos";
    if (platform.indexOf("linux") !== -1 || ua.indexOf("linux") !== -1) return "linux";
    return "unknown";
  }

  var OS_LABELS = {
    windows: "Windows",
    macos: "macOS",
    linux: "Linux",
    android: "Android",
    ios: "iOS",
    unknown: "your OS"
  };

  function showMessage(text) {
    var el = document.getElementById("direct-download-msg");
    if (!el) {
      alert(text);
      return;
    }
    el.textContent = text;
    el.style.display = "block";
  }

  window.implantDirectDownload = function (event) {
    if (event) event.preventDefault();

    var releases = window.IMPLANT_RELEASES;
    var os = detectOS();
    var url = releases && releases.platforms && releases.platforms[os];

    var msgEl = document.getElementById("direct-download-msg");
    if (msgEl) msgEl.style.display = "none";

    if (url) {
      window.location.href = url;
      return false;
    }

    showMessage(
      "No pre-built " + OS_LABELS[os] + " release is available yet. " +
      "Check the Download page for what's currently published, or run IMPLAnT from source (see the Installation guide)."
    );
    return false;
  };
})();

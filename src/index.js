// Serve the static site; send www. and plain-http visitors to https://<main domain>.
const CANONICAL = "rapidemergencyresponse.co.uk";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const onOurDomain = url.hostname === CANONICAL || url.hostname === `www.${CANONICAL}`;
    if (onOurDomain && (url.hostname !== CANONICAL || url.protocol === "http:")) {
      url.hostname = CANONICAL;
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};

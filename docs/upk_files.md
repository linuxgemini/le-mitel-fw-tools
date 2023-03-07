# Aastra/DeTeWe Magick Firmware Protection!1!1!!!

`updatetool600d.exe` has 2 options to feed it "packet sources":
  - by having `.upk` files within the same folder the executable is in
  - or by launching the executable with a flag that does... ftp (haven't figured this one out)

The `.upk` file is actually a ZIP archive with Zip 2.0/PKZIP 2/legacy password protection. The archive will also contain a comment thats like `$$randomhexstrings$$`.

So about that comment.

## where the hell is the password for this fucking zip

**extreme tl;dr,** its `xor(THATrandomhexstrings, "7f044e1c91727f207f044e1c91727f20")` which results in `{ANUUIDHERE}`; _but_ the update tool won't do an uuid check sooo yeah.

much longer explanation in node.js flavored javascript below:

```js
const { Buffer } = require("node:buffer");

/**
 * XOR a Buffer (buf) with another Buffer (key) as key material.
 *
 * If key Buffer is larger than the buf Buffer,
 * the key will be truncated to the length of
 * the buf Buffer.
 *
 * If the key Buffer is smaller than the buf Buffer,
 * the key will be "enlarged" to the length of the buf
 * Buffer by repeating the key Buffer byte by byte.
 *
 * The following example assumes that the strings represent the buffers:
 *
 * if buf is "abcd" and key is "12345", key will be truncated to "1234"
 * if buf is "abcd" and key is "12", key will be "enlarged" to "1212"
 *
 * @param {Buffer} buf The content to XOR, as a Buffer
 * @param {Buffer} key The key for XOR operation, as a Buffer
 * @returns {Buffer} buf, XOR'ed with key
 */
const xor = (buf, key) => {
    let keyToUse;

    if (key.length > buf.length) {
        keyToUse = key.subarray(0, buf.length);
    } else if (key.length < buf.length) {
        keyToUse = Buffer.alloc(buf.length, key);
    } else {
        keyToUse = key;
    }

    return buf.map((byte, index) => byte ^ keyToUse[index]);
};


const actualAastraUpkZipCommentString = "$$04367629a9144e451c297d29f71652144a3c7831f0464b43523c7c2ef34b49144a627e2ff00f$$";
const actualAastraUpkZipCommentKey = Buffer.from(actualAastraUpkZipCommentString.match(/^\$\$([0-9a-fA-F]{76})\$\$$/)[1], "hex");

const updaterXORKey = Buffer.from("7f044e1c91727f207f044e1c91727f20", "hex");

const upkZipCommentXOR = xor(actualAastraUpkZipCommentKey, updaterXORKey);

const upkZipPassword = upkZipCommentXOR.toString("hex");
const upkZipPasswordString = upkZipCommentXOR.toString();

// will return true
console.log(upkZipPassword === "7b32383538663165632d333566642d343538362d613434632d3832326239363435663033617d");

// will return true
console.log(upkZipPasswordString === "{2858f1ec-35fd-4586-a44c-822b9645f03a}");
```

the funniest shit is; the uuid is never checked. so you can just forge fw packages to flash with the update tool.

anyway linuxgemini out, i'm tired
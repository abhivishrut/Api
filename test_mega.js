const { File } = require('megajs')

async function test() {
  const folder = File.fromURL('https://mega.nz/folder/UixTVYKS#qGFMGSi0g1TVHPNgTgMCZw')
  await folder.loadAttributes()
  
  const file = folder.children.find(f => !f.directory)
  if (file) {
      try {
          const link = await file.link({ noKey: false });
          console.log("link() returned:", link)
      } catch (e) {
          console.log("link error:", e.message)
      }
      console.log("downloadId:", file.downloadId)
      console.log("key:", file.key ? file.key.toString('base64url') : "none")
      console.log("h:", file.h)
  }
}
test().catch(console.error)

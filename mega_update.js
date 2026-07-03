const { File } = require('megajs')
const fs = require('fs')

async function updateBhajans() {
  console.log('Loading MEGA folder...')
  // The MEGA folder URL
  const folder = File.fromURL('https://mega.nz/folder/UixTVYKS#qGFMGSi0g1TVHPNgTgMCZw')
  
  await folder.loadAttributes()
  console.log('Folder loaded. Files count:', folder.children.length)
  
  // Create a map of filename -> MEGA file URL
  const fileUrlMap = new Map()
  
  for (const file of folder.children) {
    if (!file.directory) {
      try {
        const link = await file.link(false) || await file.link({});
        fileUrlMap.set(file.name, link)
        fileUrlMap.set(file.name.replace(/\.[^/.]+$/, ""), link)
      } catch (e) {
         try {
             const link = await file.link({ noKey: false });
             fileUrlMap.set(file.name, link)
             fileUrlMap.set(file.name.replace(/\.[^/.]+$/, ""), link)
         } catch (e2) {
             console.log("Failed to get link for", file.name, e2.message);
         }
      }
    }
  }
  
  console.log('Generated URLs for all files.')
  
  // Read JSON
  const jsonPath = 'c:/Users/DMT/Documents/GitHub/Api/Bhajans.json'
  let rawData = fs.readFileSync(jsonPath, 'utf8')
  if (rawData.charCodeAt(0) === 0xFEFF) {
      rawData = rawData.slice(1);
  }
  const data = JSON.parse(rawData)
  
  let matchCount = 0
  let missingCount = 0
  
  for (const cat of data) {
    if (cat.bhajans) {
      for (const song of cat.bhajans) {
        let megaUrl = fileUrlMap.get(song.file_name)
        if (!megaUrl) megaUrl = fileUrlMap.get(song.title + '.mp3')
        if (!megaUrl) megaUrl = fileUrlMap.get(song.title)
        
        if (megaUrl) {
          song.audio_url = megaUrl
          matchCount++
        } else {
          missingCount++
        }
      }
    }
  }
  
  console.log(`Matched: ${matchCount}, Missing: ${missingCount}`)
  
  fs.writeFileSync(jsonPath, JSON.stringify(data, null, 4), 'utf8')
  console.log('Bhajans.json updated.')
}

updateBhajans().catch(console.error)

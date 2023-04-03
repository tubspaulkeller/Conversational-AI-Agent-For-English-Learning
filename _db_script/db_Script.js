async function getActionEvents(db, collectionName) {
  const collection = db.collection(collectionName);
  const query = { events: { $elemMatch: { event: "user" } } };
  const projection = { _id: 0, events: { $elemMatch: { event: "user" } } };
  const result = await collection.find(query, projection).toArray();
  return result;
}

const { MongoClient } = require("mongodb");
const uri =
  "mongodb+srv://tubspkeller:companiondev+1@cluster0.wox1fna.mongodb.net/?retryWrites=true&w=majority";

const client = new MongoClient(uri);

async function main() {
  try {
    await client.connect();
    const database = client.db("rasa_ben");
    const collectionName = "conversations";
    const actionEvents = await getActionEvents(database, collectionName);
    console.log(actionEvents);
  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

main();

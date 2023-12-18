#Импортируйте модуль в файле с бизнес-логикой бронирования
#(например, `bookingService.js`) и использовать его для индексации свободных дат

const elasticClient = require('./elasticsearch');

async function saveBooking(bookingData) {
     # Сохранить бронь в MongoDB

     # Индексировать свободные даты в Elasticsearch
     const { fromDate, toDate } = bookingData;
     const room = bookingData.room;

    const
    body = {
        room,
        fromDate,
        toDate
    };

    await elasticClient.index({
       index: 'bookings',
       body
     });
   }

#Пример поиска свободных комнат по датам в Elasticsearch:

async function searchAvailableRooms(fromDate, toDate) {
     const { body } = await elasticClient.search({
       index: 'bookings',
       body: {
         query: {
           bool: {
             must: [
               { range: { fromDate: { gte: fromDate } } },
               { range: { toDate: { lte: toDate } } }
             ]
           }
         }
       }
     });

     return body.hits.hits.map(hit => hit._source.roomId);
   }


#после сохранения данных в MongoDB - логика индексирования этих данных в ElasticSearch.
# Например,  индексировать свободные даты бронирования, после
# сохранения брони надо следующий код:

# Индексирование свободных дат в ElasticSearch
const indexData = {
  index: 'reservations',
  body: {
    date: newReservation.date, # Здесь необходимо указать свойство, где хранится свободная дата
    # Другие свойства для поиска (описание, адрес, и т.д.)
  },
};

await client.index(indexData);

#логика поиска свободных комнат в ElasticSearch.
#Например, если пользователь ищет комнаты по описанию и адресу

# Поиск свободных комнат по описанию и адресу
const searchData = {
  index: 'reservations',
  body: {
    query: {
      bool: {
        must: [
          { match: { description: 'поиск по описанию' } }, # Здесь нужно указать свойства, по которым будет поиск
          { match: { address: 'поиск по адресу' } }
        ]
      }
    }
  }
};

const searchResults = await client.search(searchData);

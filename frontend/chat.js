import fetch from 'node-fetch'
import dotenv from 'dotenv'

dotenv.config()

export const chat = async (question) => {
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
      model: 'gpt-3.5-turbo'
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: question }]
    })
  })
  const data = await res.json()
  return data.choices[0].message.content
}
// function chat (question) {
//   return fetch('https://api.openai.com/v1/chat/completions', {
//     method: 'POST',
//     headers: {
//       Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
//       'Content-Type': 'application/json',
//       model: 'gpt-3.5-turbo'
//     },
//     body: JSON.stringify({
//       model: 'gpt-3.5-turbo',
//       messages: [{ role: 'user', content: question }]
//     })
//   })
//     .then((res) => res.json())
//     .then((data) => data.choices[0].message.content)
// }

// chat('안녕').then((answer) => console.log(answer))

// console.log(chat('안녕'))

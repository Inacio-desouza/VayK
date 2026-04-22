import { tripStore } from '../stores/tripStores'

function parseArrivalDate() {
  const match = tripStore.tripDates.match(/^(\d{4}-\d{2}-\d{2})/)
  if (match) return match[1]
  return tripStore.tripForm.arrivalDate || null
}

function getDayDate(arrivalISO, dayNumber) {
  const date = new Date(arrivalISO + 'T00:00:00')
  date.setDate(date.getDate() + (dayNumber - 1))
  return date
}

function formatICSDate(date, hours, minutes) {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  const h = String(hours).padStart(2, '0')
  const min = String(minutes).padStart(2, '0')
  return `${y}${m}${d}T${h}${min}00`
}

function parseTime12h(timeStr) {
  if (!timeStr) return null

  const cleaned = timeStr.split('-')[0].trim().toUpperCase()
  const match = cleaned.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/)
  if (!match) return null

  let hours = Number(match[1])
  const minutes = Number(match[2])
  const meridiem = match[3]

  if (meridiem === 'AM' && hours === 12) hours = 0
  if (meridiem === 'PM' && hours !== 12) hours += 12

  return { hours, minutes, totalMinutes: hours * 60 + minutes }
}

function escapeICS(text) {
  if (!text) return ''
  return text.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n')
}

function findUntimedSlots(timedActivities, untimedCount) {
  const slots = []
  const SLOT_DURATION = 30

  const occupied = timedActivities
    .map((a) => {
      const parsed = parseTime12h(a.time)
      if (!parsed) return null
      return { start: parsed.totalMinutes, end: parsed.totalMinutes + 60 }
    })
    .filter(Boolean)
    .sort((a, b) => a.start - b.start)

  // Try to fill gaps between timed activities first, then append after the last one
  const gaps = []

  // Gap before first activity (starting at 8 AM = 480 min)
  const dayStart = 480
  const dayEnd = 1320 // 10 PM

  if (occupied.length === 0) {
    gaps.push({ start: dayStart, end: dayEnd })
  } else {
    if (occupied[0].start > dayStart) {
      gaps.push({ start: dayStart, end: occupied[0].start })
    }
    for (let i = 0; i < occupied.length - 1; i++) {
      if (occupied[i].end < occupied[i + 1].start) {
        gaps.push({ start: occupied[i].end, end: occupied[i + 1].start })
      }
    }
    if (occupied[occupied.length - 1].end < dayEnd) {
      gaps.push({ start: occupied[occupied.length - 1].end, end: dayEnd })
    }
  }

  let placed = 0
  for (const gap of gaps) {
    if (placed >= untimedCount) break
    let cursor = gap.start
    while (cursor + SLOT_DURATION <= gap.end && placed < untimedCount) {
      slots.push({ hours: Math.floor(cursor / 60), minutes: cursor % 60 })
      cursor += SLOT_DURATION
      placed++
    }
  }

  return slots
}

function buildICS() {
  const arrivalISO = parseArrivalDate()
  if (!arrivalISO) return null

  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//VayK//Trip Itinerary//EN',
    'CALSCALE:GREGORIAN',
  ]

  for (const day of tripStore.days) {
    const dayDate = getDayDate(arrivalISO, day.dayNumber)
    const timed = day.activities.filter((a) => a.time)
    const untimed = day.activities.filter((a) => !a.time)

    // Timed activities
    for (const activity of timed) {
      const parsed = parseTime12h(activity.time)
      if (!parsed) continue

      const dtStart = formatICSDate(dayDate, parsed.hours, parsed.minutes)
      const endH = parsed.hours + 1
      const dtEnd = formatICSDate(dayDate, endH, parsed.minutes)

      lines.push('BEGIN:VEVENT')
      lines.push(`DTSTART:${dtStart}`)
      lines.push(`DTEND:${dtEnd}`)
      lines.push(`SUMMARY:${escapeICS(activity.name || activity.title)}`)
      if (activity.address) lines.push(`LOCATION:${escapeICS(activity.address)}`)
      if (activity.description || activity.rating) {
        const desc = [activity.description, activity.rating ? `Rating: ${activity.rating}` : '']
          .filter(Boolean)
          .join('\\n')
        lines.push(`DESCRIPTION:${escapeICS(desc)}`)
      }
      lines.push('END:VEVENT')
    }

    // Untimed activities — slot into gaps
    const slots = findUntimedSlots(timed, untimed.length)
    for (let i = 0; i < untimed.length; i++) {
      const activity = untimed[i]
      const slot = slots[i]
      if (!slot) break

      const dtStart = formatICSDate(dayDate, slot.hours, slot.minutes)
      const endMin = slot.hours * 60 + slot.minutes + 30
      const dtEnd = formatICSDate(dayDate, Math.floor(endMin / 60), endMin % 60)

      lines.push('BEGIN:VEVENT')
      lines.push(`DTSTART:${dtStart}`)
      lines.push(`DTEND:${dtEnd}`)
      lines.push(`SUMMARY:${escapeICS(activity.name || activity.title)}`)
      if (activity.address) lines.push(`LOCATION:${escapeICS(activity.address)}`)
      if (activity.description || activity.rating) {
        const desc = [activity.description, activity.rating ? `Rating: ${activity.rating}` : '']
          .filter(Boolean)
          .join('\\n')
        lines.push(`DESCRIPTION:${escapeICS(desc)}`)
      }
      lines.push('END:VEVENT')
    }
  }

  lines.push('END:VCALENDAR')
  return lines.join('\r\n')
}

export function downloadICS() {
  const ics = buildICS()
  if (!ics) return

  const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${tripStore.tripTitle || 'trip'}.ics`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

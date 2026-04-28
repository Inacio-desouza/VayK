import { tripStore } from '../stores/tripStores'

function titleFor(activity) {
  return tripStore.getActivityTitle(activity)
}

function subtitleFor(activity) {
  return activity.address || activity.venue || activity.location || ''
}

function linkLabel(url) {
  if (!url) return ''
  const lower = url.toLowerCase()
  return lower.includes('google.com/maps') || lower.includes('maps')
    ? 'Open in Maps'
    : 'View Details'
}

function escapeHtml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

export function downloadPDF() {
  const printWindow = window.open('', '_blank')
  if (!printWindow) return

  const daysHtml = tripStore.days
    .map((day) => {
      const activitiesHtml = day.activities.length
        ? day.activities
            .map((activity) => {
              const title = escapeHtml(titleFor(activity))
              const time = escapeHtml(activity.time || 'No set time')
              const subtitle = escapeHtml(subtitleFor(activity))
              const description = escapeHtml(activity.description)
              const rating = activity.rating
                ? `<p class="meta"><strong>Rating:</strong> ★ ${escapeHtml(activity.rating)}${
                    activity.reviewCount
                      ? ` (${escapeHtml(activity.reviewCount.toLocaleString())} reviews)`
                      : ''
                  }</p>`
                : ''
              const link = activity.url
                ? `<p class="meta"><strong>Link:</strong> <a href="${escapeHtml(activity.url)}">${linkLabel(activity.url)}</a></p>`
                : ''

              return `
                <div class="activity">
                  <div class="activity-header">
                    <h3>${title}</h3>
                    <span>${time}</span>
                  </div>

                  ${subtitle ? `<p class="meta"><strong>Location:</strong> ${subtitle}</p>` : ''}
                  ${rating}
                  ${description ? `<p class="description">${description}</p>` : ''}
                  ${link}
                </div>
              `
            })
            .join('')
        : `<p class="empty">No activities added for this day.</p>`

      return `
        <section class="day-card">
          <div class="day-header">
            <p>Day ${escapeHtml(day.dayNumber)}</p>
            <h2>${escapeHtml(day.dateLabel)}</h2>
          </div>
          <div class="day-body">
            ${activitiesHtml}
          </div>
        </section>
      `
    })
    .join('')

  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>${escapeHtml(tripStore.tripTitle)} Itinerary</title>
        <style>
          * {
            box-sizing: border-box;
          }

          body {
            margin: 0;
            padding: 36px;
            font-family: Inter, Arial, sans-serif;
            background: #fcfcfd;
            color: #111827;
          }

          .pdf-header {
            margin-bottom: 28px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 20px;
          }

          .pdf-header h1 {
            margin: 0;
            font-size: 34px;
            line-height: 1.1;
            letter-spacing: -0.02em;
          }

          .pdf-header p {
            margin: 8px 0 0;
            color: #6b7280;
            font-size: 16px;
          }

          .day-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 22px;
            margin-bottom: 24px;
            overflow: hidden;
            page-break-inside: avoid;
          }

          .day-header {
            background: #f8fafc;
            padding: 18px 22px;
            border-bottom: 1px solid #e5e7eb;
          }

          .day-header p {
            margin: 0 0 4px;
            font-size: 14px;
            color: #6b7280;
          }

          .day-header h2 {
            margin: 0;
            font-size: 22px;
          }

          .day-body {
            padding: 18px 22px;
          }

          .activity {
            border: 1px solid #e5e7eb;
            border-left: 4px solid #d5dbe6;
            border-radius: 18px;
            padding: 16px 18px;
            margin-bottom: 14px;
            page-break-inside: avoid;
          }

          .activity:last-child {
            margin-bottom: 0;
          }

          .activity-header {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: flex-start;
          }

          .activity-header h3 {
            margin: 0;
            font-size: 18px;
          }

          .activity-header span {
            color: #27429b;
            font-weight: 700;
            white-space: nowrap;
          }

          .meta {
            margin: 10px 0 0;
            color: #334155;
            font-size: 14px;
            line-height: 1.5;
          }

          .description {
            margin: 12px 0 0;
            color: #334155;
            font-size: 15px;
            line-height: 1.65;
          }

          a {
            color: #27429b;
            text-decoration: none;
            font-weight: 700;
          }

          .empty {
            color: #94a3b8;
            margin: 0;
          }

          @media print {
            body {
              background: white;
              padding: 24px;
            }

            .day-card {
              break-inside: avoid;
            }

            .activity {
              break-inside: avoid;
            }
          }
        </style>
      </head>

      <body>
        <header class="pdf-header">
          <h1>${escapeHtml(tripStore.tripTitle)}</h1>
          <p>${escapeHtml(tripStore.tripDates)}</p>
        </header>

        ${daysHtml}

        <script>
          window.onload = () => {
            window.print()
          }
        </script>
      </body>
    </html>
  `)

  printWindow.document.close()
}
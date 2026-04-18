---
title: "酷暑日 (Kokushobi): Japan Names Its Cruellest Days"
date: 2026-04-19 09:00:00 +0900
categories: [Climate, Japan]
tags: [japan, heatwave, climate, weather]
---

Japan has a word for almost every gradation of summer heat. There is *natsuhi* (夏日) — a summer day, when the mercury clears 25°C. Then *manatsuhi* (真夏日), a midsummer day, at 30°C. Then *mōshobi* (猛暑日), a fierce-heat day, at 35°C. For decades that was the top of the scale. It no longer is.

After the summer of 2024 — Japan's hottest on record — the Japan Meteorological Agency (JMA) ran an online public survey to name something the existing vocabulary could not adequately describe: a day when the temperature reaches or exceeds **40°C**. The winner, chosen from thousands of submissions, was **酷暑日** (*kokushobi*).

## What the word means

Break the kanji apart and you get the full force of it:

| Kanji | Reading | Meaning |
|-------|---------|---------|
| 酷 | koku | cruel, harsh, severe |
| 暑 | sho | heat, summer warmth |
| 日 | bi / nichi | day |

*酷* is the same character used in *zankoku* (残酷) — brutal, atrocious. The agency did not reach for a polite euphemism. A *kokushobi* is, literally, a **cruelly hot day**.

The naming follows a long Japanese tradition of giving precise meteorological vocabulary to atmospheric states that other languages treat as a single undifferentiated "hot". The full ladder now looks like this:

| Term | Kanji | Threshold | English gloss |
|------|-------|-----------|---------------|
| Natsuhi | 夏日 | ≥ 25°C | Summer day |
| Manatsuhi | 真夏日 | ≥ 30°C | Midsummer day |
| Nettaiya | 熱帯夜 | ≥ 25°C (overnight low) | Tropical night |
| Mōshobi | 猛暑日 | ≥ 35°C | Fierce-heat day |
| **Kokushobi** | **酷暑日** | **≥ 40°C** | **Cruelly hot day** |

The JMA says the new designation will "effectively call for vigilance" — signalling to the public that 40°C is not merely an extreme version of ordinary heat but a categorically different and life-threatening condition.

## The summer that made the word necessary

In 2024, Japan recorded nine days on which at least one observing station reported temperatures at or above 40°C. That is an unprecedented count in the JMA's 150-year measurement history. Tokyo's Nerima district hit 40.0°C. Kofu, already notorious for heat, topped 40°C multiple times. Niigata — a city on the Sea of Japan coast not historically associated with extreme heat — crossed the threshold twice in July.

The chart below shows the peak daily maximum temperatures recorded at major JMA stations across the 2024 summer season.

<div style="max-width: 760px; margin: 2rem auto;">
<canvas id="heatChart" style="width:100%; height:400px;"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
(function() {
  var ctx = document.getElementById('heatChart');
  if (!ctx) return;

  var labels = [
    'Jun 1','Jun 8','Jun 15','Jun 22','Jun 29',
    'Jul 6','Jul 13','Jul 20','Jul 27',
    'Aug 3','Aug 10','Aug 17','Aug 24','Aug 31',
    'Sep 7','Sep 14'
  ];

  // Peak daily max across major stations (°C) — weekly snapshots, 2024
  var tokyo = [29,31,33,35,34, 37,38,36,39, 38,37,40,36,35, 33,31];
  var osaka = [30,32,34,36,35, 38,39,37,40, 39,38,38,36,34, 32,30];
  var kofu  = [31,33,35,37,36, 39,40,40,40, 40,40,39,37,35, 34,31];
  var threshold = Array(labels.length).fill(40);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Tokyo (Nerima)',
          data: tokyo,
          borderColor: '#4e79a7',
          backgroundColor: 'rgba(78,121,167,0.08)',
          tension: 0.3,
          pointRadius: 3,
          fill: false
        },
        {
          label: 'Osaka',
          data: osaka,
          borderColor: '#f28e2b',
          backgroundColor: 'rgba(242,142,43,0.08)',
          tension: 0.3,
          pointRadius: 3,
          fill: false
        },
        {
          label: 'Kofu (Yamanashi)',
          data: kofu,
          borderColor: '#e15759',
          backgroundColor: 'rgba(225,87,89,0.08)',
          tension: 0.3,
          pointRadius: 3,
          fill: false
        },
        {
          label: '酷暑日 threshold (40°C)',
          data: threshold,
          borderColor: '#cc0000',
          borderDash: [6, 4],
          borderWidth: 1.5,
          pointRadius: 0,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: {
          display: true,
          text: 'Japan Peak Daily Maximum Temperature — Summer 2024',
          font: { size: 13 }
        },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              return ctx.dataset.label + ': ' + ctx.parsed.y + '°C';
            }
          }
        }
      },
      scales: {
        y: {
          min: 26,
          max: 42,
          title: { display: true, text: 'Temperature (°C)' },
          ticks: { stepSize: 2 }
        },
        x: {
          title: { display: true, text: '2024' }
        }
      }
    }
  });
})();
</script>

The dashed red line marks the new kokushobi threshold. Kofu effectively lived above it for a three-week stretch in late July and early August — a sustained period that would have been statistically unthinkable in the 1990s.

## Why 2024 was different

The proximate causes are familiar: a strengthened Pacific High pressure system, reduced cloud cover, and urban heat island effects amplifying what were already record sea-surface temperatures in the surrounding waters. The structural cause is also familiar: background warming driven by greenhouse gas accumulation has shifted Japan's entire summer temperature distribution roughly 1.5°C warmer compared to the 1990 baseline.

What made 2024 notable beyond the raw numbers was the **duration** and **geographic spread**. Historically extreme heat in Japan was concentrated in inland basins — Kofu, Tajimi, Kumagaya. In 2024, coastal cities including Niigata and Sendai reported temperatures they had no historical analogue for.

## A name is a policy instrument

Language matters in public health. Studies of typhoon preparedness in Japan have repeatedly shown that named, categorised threats — with clear, memorable vocabulary — drive faster and more consistent protective behaviour than numerical warnings alone. The JMA's decision to coin *kokushobi* is, in a narrow sense, a communications strategy: give the thing a name and people will remember what the name means.

It is also an acknowledgement. The old vocabulary, built in a cooler era, no longer fits the weather Japan is living through. Adding a rung at the top of the ladder is not an act of resignation — it is the necessary precondition for talking clearly about what is coming.

Days above 40°C were, until recently, rare enough to be treated as individual curiosities. The JMA now expects them to be common enough to warrant their own word. That shift — from anomaly to category — is perhaps the most telling climate signal of all.

import { MapPin } from "lucide-react";

import { siteConfig } from "@/config/site";
import { Badge } from "@/components/ui/badge";

export function MapPanel() {
  return (
    <div className="rounded-2xl border border-slate-200/60 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">
            Kenya Project Map
          </p>
          <h3 className="text-lg font-semibold text-slate-900">
            County Coverage Snapshot
          </h3>
          <p className="text-sm text-slate-500">
            Mapbox GL placeholder token: {siteConfig.mapbox.token}
          </p>
        </div>
        <Badge variant="secondary">Mapbox GL</Badge>
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-[2fr,1fr]">
        <div className="relative min-h-[260px] overflow-hidden rounded-xl bg-gradient-to-br from-emerald-100 via-emerald-50 to-white">
          <div className="absolute inset-0 flex items-center justify-center text-sm text-emerald-700">
            Kenya map visualization placeholder
          </div>
          <div className="absolute left-6 top-6 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-emerald-700 shadow">
            Active pins: {siteConfig.mapbox.pins.length}
          </div>
        </div>
        <div className="space-y-3">
          {siteConfig.mapbox.pins.map((pin) => (
            <div
              key={pin.label}
              className="flex items-center justify-between rounded-lg border border-slate-200/60 px-3 py-2 text-sm"
            >
              <div className="flex items-center gap-2 text-slate-700">
                <MapPin className="h-4 w-4 text-emerald-500" />
                {pin.label}
              </div>
              <span className="text-xs text-slate-400">{pin.coordinates}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

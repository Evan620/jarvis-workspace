import { siteConfig } from "@/config/site";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

export function FilterSidebar() {
  return (
    <aside className="space-y-6 rounded-2xl border border-slate-200/60 bg-white p-6 shadow-sm">
      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Filter Projects
        </h3>
        <p className="text-xs text-slate-400">
          Narrow the pipeline with sector, stage, and ticket size.
        </p>
      </div>
      <div className="space-y-2">
        <Label htmlFor="search">Search by keyword</Label>
        <Input id="search" placeholder="Cold chain, irrigation..." />
      </div>
      <Separator />
      <div className="space-y-3">
        <Label className="text-xs uppercase tracking-wide text-slate-500">
          Sector Focus
        </Label>
        <div className="space-y-2">
          {siteConfig.filters.sectors.map((sector) => (
            <label key={sector} className="flex items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" className="h-4 w-4 rounded border-slate-300" />
              {sector}
            </label>
          ))}
        </div>
      </div>
      <Separator />
      <div className="space-y-3">
        <Label className="text-xs uppercase tracking-wide text-slate-500">
          Investment Stage
        </Label>
        <div className="space-y-2">
          {siteConfig.filters.stages.map((stage) => (
            <label key={stage} className="flex items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" className="h-4 w-4 rounded border-slate-300" />
              {stage}
            </label>
          ))}
        </div>
      </div>
      <Separator />
      <div className="space-y-3">
        <Label className="text-xs uppercase tracking-wide text-slate-500">
          Ticket Size
        </Label>
        <div className="space-y-2">
          {siteConfig.filters.ticketSizes.map((ticket) => (
            <label key={ticket} className="flex items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" className="h-4 w-4 rounded border-slate-300" />
              {ticket}
            </label>
          ))}
        </div>
      </div>
    </aside>
  );
}

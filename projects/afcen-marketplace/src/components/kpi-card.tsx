import { Card, CardContent, CardHeader } from "@/components/ui/card";

interface KpiCardProps {
  label: string;
  value: string;
  delta: string;
}

export function KpiCard({ label, value, delta }: KpiCardProps) {
  return (
    <Card>
      <CardHeader className="space-y-1">
        <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
        <p className="text-2xl font-semibold text-slate-900">{value}</p>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-emerald-600">{delta}</p>
      </CardContent>
    </Card>
  );
}

import { LandingHero } from '@/app/components/landing-hero';
import { LandingFeatures } from '@/app/components/landing-features';
import { LandingCTA } from '@/app/components/landing-cta';

export default function Home() {
  return (
    <main className="min-h-screen">
      <LandingHero />
      <LandingFeatures />
      <LandingCTA />
    </main>
  );
}

'use client';

/**
 * AI Roadmap Generator Page
 * 
 * Generate personalized learning roadmaps using AI
 */

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Sparkles, 
  X, 
  Plus, 
  Loader2,
  BookOpen,
  Calendar,
  Target
} from 'lucide-react';
import { generateRoadmap } from '@/app/api/ai';
import ReactMarkdown from 'react-markdown';

export default function RoadmapPage() {
  const [skills, setSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState('');
  const [manualSkills, setManualSkills] = useState('');

  const mutation = useMutation({
    mutationFn: (skillsList: string[]) => generateRoadmap(skillsList),
  });

  const addSkill = () => {
    const trimmed = skillInput.trim();
    if (trimmed && !skills.includes(trimmed)) {
      setSkills([...skills, trimmed]);
      setSkillInput('');
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setSkills(skills.filter(skill => skill !== skillToRemove));
  };

  const handleManualSkills = () => {
    const skillsList = manualSkills
      .split(/[,\n]/)
      .map(s => s.trim())
      .filter(s => s.length > 0);
    
    if (skillsList.length > 0) {
      setSkills([...new Set([...skills, ...skillsList])]);
      setManualSkills('');
    }
  };

  const handleGenerate = () => {
    if (skills.length > 0) {
      mutation.mutate(skills);
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Roadmap Generator</h1>
        <p className="text-gray-600">Create a personalized 4-week learning roadmap for your target skills</p>
      </div>

      {/* Input Section */}
      <div className="grid gap-6 md:grid-cols-2 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Add Skills</CardTitle>
            <CardDescription>Enter skills you want to learn</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Python, Machine Learning..."
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    addSkill();
                  }
                }}
              />
              <Button
                onClick={addSkill}
                disabled={!skillInput.trim()}
                className="bg-[#0077B5] hover:bg-[#004182]"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            {skills.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {skills.map((skill) => (
                  <Badge
                    key={skill}
                    variant="secondary"
                    className="text-sm py-1 px-3 flex items-center gap-2"
                  >
                    {skill}
                    <button
                      onClick={() => removeSkill(skill)}
                      className="ml-1 hover:text-red-600"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Bulk Import</CardTitle>
            <CardDescription>Paste a list of skills (comma or newline separated)</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <textarea
              className="w-full min-h-[100px] p-3 border border-gray-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-[#0077B5] focus:border-transparent"
              placeholder="Python&#10;Machine Learning&#10;Data Science"
              value={manualSkills}
              onChange={(e) => setManualSkills(e.target.value)}
            />
            <Button
              onClick={handleManualSkills}
              disabled={!manualSkills.trim()}
              variant="outline"
              className="w-full"
            >
              Add Skills
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Generate Button */}
      <Card className="mb-8">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">
                {skills.length > 0 
                  ? `Ready to generate roadmap for ${skills.length} skill${skills.length === 1 ? '' : 's'}`
                  : 'Add at least one skill to generate a roadmap'}
              </p>
              {skills.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {skills.map((skill) => (
                    <Badge key={skill} variant="outline" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
            <Button
              onClick={handleGenerate}
              disabled={skills.length === 0 || mutation.isPending}
              className="bg-[#0077B5] hover:bg-[#004182] px-8"
            >
              {mutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate Roadmap
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Error Display */}
      {mutation.isError && (
        <Card className="mb-8 border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="space-y-2">
              <p className="text-red-800 font-semibold">❌ Failed to generate roadmap</p>
              <p className="text-red-600 text-sm">
                {mutation.error instanceof Error ? mutation.error.message : 'Unknown error occurred'}
              </p>
              {mutation.error instanceof Error && mutation.error.message.includes('Network') && (
                <div className="mt-4 p-3 bg-red-100 rounded border border-red-200">
                  <p className="text-red-700 text-sm font-medium mb-2">Connection Issue:</p>
                  <ul className="text-red-600 text-xs list-disc list-inside space-y-1">
                    <li>Make sure the backend server is running on port 8001</li>
                    <li>Check that your .env.local has: NEXT_PUBLIC_API_URL=http://127.0.0.1:8001</li>
                    <li>Restart your frontend server after changing .env.local</li>
                    <li>Check the browser console for more details</li>
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Roadmap Display */}
      {mutation.isSuccess && mutation.data && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-2xl mb-2">Your Learning Roadmap</CardTitle>
                <CardDescription>
                  {mutation.data.message} • {mutation.data.skills.length} skill{mutation.data.skills.length === 1 ? '' : 's'}
                </CardDescription>
              </div>
              <Badge className="bg-green-100 text-green-800">
                <Target className="h-3 w-3 mr-1" />
                Ready
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="prose prose-sm max-w-none">
              <div className="markdown-content">
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-2xl font-bold text-gray-900 mt-6 mb-4">{children}</h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-xl font-semibold text-gray-900 mt-5 mb-3">{children}</h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-lg font-medium text-gray-900 mt-4 mb-2">{children}</h3>
                    ),
                    p: ({ children }) => (
                      <p className="text-gray-700 mb-3 leading-relaxed">{children}</p>
                    ),
                    ul: ({ children }) => (
                      <ul className="list-disc list-inside mb-4 space-y-2 text-gray-700">{children}</ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="list-decimal list-inside mb-4 space-y-2 text-gray-700">{children}</ol>
                    ),
                    li: ({ children }) => (
                      <li className="ml-4">{children}</li>
                    ),
                    strong: ({ children }) => (
                      <strong className="font-semibold text-gray-900">{children}</strong>
                    ),
                    code: ({ children }) => (
                      <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-[#0077B5]">
                        {children}
                      </code>
                    ),
                  }}
                >
                  {mutation.data.roadmap}
                </ReactMarkdown>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {!mutation.isSuccess && !mutation.isPending && (
        <Card>
          <CardContent className="pt-6 text-center py-12">
            <Sparkles className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Generate Your Roadmap</h3>
            <p className="text-gray-600">
              Add skills above and click "Generate Roadmap" to create your personalized learning plan.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

